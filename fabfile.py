import getpass
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style
from django.template import Context, Engine
from dotenv import load_dotenv
from fabric import Config, Connection, task

load_dotenv()

HOST = os.getenv("PROD_HOST")
USER = os.getenv("PROD_USER")
NGINX_SERVER_NAME = os.getenv("PROD_NGINX_SERVER_NAME")

if not HOST or not USER or not NGINX_SERVER_NAME:
    print(
        "Please set PROD_HOST, PROD_USER, PROD_NGINX_SERVER_NAME environment variables."
    )
    sys.exit(1)

HOME = f"/home/{USER}"

CURRENT_RELEASE = "release-current"

ENV = {"DJANGO_SETTINGS_MODULE": "notcms.settings.prod"}

BASE_DIR = Path(__file__).resolve().parent


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def render_template(template_path, context):
    engine = Engine()

    with open(template_path) as file:
        template_content = file.read()

    template = engine.from_string(template_content)
    return template.render(Context(context))


def get_remote():
    return Connection(HOST)


def get_remote_superuser():
    sudo_pass = getpass.getpass("[sudo] password: ")
    config = Config(overrides={"sudo": {"password": sudo_pass}})
    return Connection(HOST, config=config)


def get_timestamp():
    return int(datetime.now().timestamp())


@contextmanager
def virtualenv(c):
    with c.prefix("source .venv/bin/activate"):
        yield


@contextmanager
def npm(c):
    with c.prefix(f'export NVM_DIR="/home/{USER}/.nvm"'):  # noqa: SIM117
        with c.prefix('source "$NVM_DIR/nvm.sh"'):
            yield


def get_releases(c):
    return c.run(
        'ls -d release-* | grep -E "release-[0-9]+" | sort -r', hide=True
    ).stdout.split()


def get_current_release_version(conn):
    result = conn.run(f"readlink {CURRENT_RELEASE}", warn=True, hide=True)

    if result.ok:
        return result.stdout.strip()
    else:
        return None


def git_pull(c):
    print("Pulling from latest master")
    c.run("git pull")


def git_clone(c):
    print("Cloning repository")
    c.run(
        "git clone --depth 1 --branch master "
        "git@github.com:bozbalci/bozbalci-blog.git ."
    )


def create_virtualenv(c):
    print("Creating virtual environment")
    c.run("python3 -m venv .venv")


def inject_secrets(c):
    print("Injecting secrets")
    c.run(f"cp {HOME}/secrets/prod.env .env")


def install_node_dependencies(c):
    with npm(c):
        print("Installing Node dependencies...")
        c.run("npm install")


def build_frontend(c):
    with npm(c):
        print("Building frontend...")
        c.run("npm run build")


def install_python_dependencies(c):
    with virtualenv(c):
        print("Installing Python dependencies...")
        c.run("pip install -r requirements.txt")


def django_collectstatic(c):
    with virtualenv(c):
        print("Collecting static assets...")
        c.run("rm -vrf staticfiles/")
        c.run("python manage.py collectstatic", env=ENV, pty=True)


def django_migrate_db(c):
    with virtualenv(c):
        print("Running database migrations...")
        c.run("python manage.py migrate", env=ENV)


def restart_wsgi(c):
    print("Restarting WSGI server")
    c.run("sudo systemctl restart gunicorn", pty=True)


def promote_version(c, release_directory):
    if query_yes_no(f"Promote version {release_directory} to current?", default="no"):
        c.run(f"ln -sfn {release_directory} {CURRENT_RELEASE}")
        restart_wsgi(c)


@task
def show(c):
    with get_remote() as conn:
        current_release_version = get_current_release_version(conn)

        for i, release in enumerate(get_releases(conn)):
            print(Fore.BLUE, end="")
            if i == 0:
                print(f"[{i}, release", end="")
            elif i == 1:
                print(f"[{i}, rollback", end="")
            else:
                print(f"[{i}", end="")

            if release == current_release_version:
                print(f", {Style.BRIGHT}current{Style.NORMAL}", end="")

            print(f"]{Fore.RESET} ", end="")

            with conn.cd(release):
                try:
                    commit_hash, commit_message = (
                        conn.run("git log -1 --pretty=format:'%h::::%s'", hide=True)
                        .stdout.strip()
                        .split("::::")
                    )

                    print(f"{Fore.YELLOW}{commit_hash}{Fore.RESET} {release}")
                    print(commit_message)
                    print()

                except Exception as e:
                    print(
                        f"{release}: Not a git repository or error occurred: {str(e)}"
                    )


@task
def deploy_incremental(c, dependencies=True, collectstatic=True, migrate=True):
    with get_remote() as conn:  # noqa: SIM117
        with conn.cd(CURRENT_RELEASE):
            git_pull(conn)
            inject_secrets(conn)
            if dependencies:
                install_node_dependencies(conn)
                install_python_dependencies(conn)
            if collectstatic:
                build_frontend(conn)
                django_collectstatic(conn)
            if migrate:
                django_migrate_db(conn)
            restart_wsgi(conn)


@task
def deploy(c, release=True):
    with get_remote() as conn:
        current_ts = get_timestamp()
        version = f"release-{current_ts}"
        release_directory = f"{HOME}/{version}"
        conn.run(f"mkdir -p {release_directory}")

        with conn.cd(release_directory):
            git_clone(conn)
            inject_secrets(conn)
            create_virtualenv(conn)
            install_node_dependencies(conn)
            install_python_dependencies(conn)
            build_frontend(conn)
            django_collectstatic(conn)
            django_migrate_db(conn)

        # If there is NO release-current already, prepare it for the gunicorn systemd
        # service
        conn.run(
            f"[ ! -L {CURRENT_RELEASE} ] && ln -sfn {version} {CURRENT_RELEASE}",
            warn=True,
        )

        if release:
            promote_version(conn, version)


@task
def release(c):
    with get_remote() as conn:
        releases = get_releases(conn)
        to_version = releases[0]
        promote_version(conn, to_version)


@task
def rollback(c, to_version=None):
    with get_remote() as conn:
        releases = get_releases(conn)

        if to_version and to_version in releases:
            promote_version(conn, to_version)
        elif to_version.isdigit():
            to_version = releases[int(to_version)]
            promote_version(conn, to_version)
        elif len(releases) > 1:
            to_version = releases[1]
            promote_version(conn, to_version)
        else:
            print("No previous release to rollback to")


@task
def push_secrets(c):
    with get_remote() as conn:
        conn.run("mkdir -p secrets")
        conn.put(BASE_DIR / "secrets" / "prod.env", "secrets")
        print("Secrets pushed to remote. Future deployments will use these secrets.")


@task
def shell(c):
    with get_remote() as conn:  # noqa: SIM117
        with virtualenv(conn):
            conn.run(
                "python manage.py shell",
                env=ENV,
                pty=True,
            )


@task
def provision(c):
    print("Rendering configuration file templates...")

    template_context = {
        "user": USER,
        "django_settings_module": ENV["DJANGO_SETTINGS_MODULE"],
        "server_name": NGINX_SERVER_NAME,
    }

    files = {
        "gunicorn.service": BASE_DIR / "config" / "gunicorn.service",
        "gunicorn.socket": BASE_DIR / "config" / "gunicorn.socket",
        "nginx.conf": BASE_DIR / "config" / "nginx.conf",
    }

    temp_files = {}
    for name, template_path in files.items():
        rendered_content = render_template(template_path, template_context)
        temp_file_path = f"/tmp/{name}"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(rendered_content)
        temp_files[name] = temp_file_path

    with get_remote() as conn:
        print("Copying files to remote...")
        for name, local_path in temp_files.items():
            conn.put(local_path, name)
            c.run(f"rm {local_path}")  # delete from local

    print("Moving files under /etc...")
    with get_remote_superuser() as conn:
        conn.sudo("mv gunicorn.socket /etc/systemd/system/gunicorn.socket", hide=True)
        conn.sudo("mv gunicorn.service /etc/systemd/system/gunicorn.service", hide=True)
        conn.sudo(
            f"mv nginx.conf /etc/nginx/sites-available/{NGINX_SERVER_NAME}", hide=True
        )
        conn.sudo("systemctl daemon-reload", hide=True)

        print("Starting and enabling gunicorn socket...")
        conn.sudo("systemctl restart gunicorn.socket", hide=True)
        conn.sudo("systemctl enable gunicorn.socket", hide=True)

        print("Starting gunicorn through socket activation...")
        conn.run("curl --unix-socket /run/gunicorn.sock localhost", hide=True)
        print("Restarting gunicorn service...")
        conn.sudo("systemctl restart gunicorn", hide=True)

        print("Enabling nginx site...")
        conn.sudo(
            f"ln -sfn /etc/nginx/sites-available/{NGINX_SERVER_NAME} "
            f"/etc/nginx/sites-enabled"
        )

        print("Allowing Nginx in ufw firewall...")
        conn.sudo("ufw allow 'Nginx Full'", hide=True)

        print("Restarting nginx service...")
        conn.sudo("systemctl restart nginx", hide=True)
