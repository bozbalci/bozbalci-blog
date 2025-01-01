import os
from contextlib import contextmanager
from datetime import datetime

from dotenv import load_dotenv
from fabric import Connection, task

load_dotenv()

HOST = os.getenv("PROD_HOST")
USER = os.getenv("PROD_USER")

HOME = f"/home/{USER}"

CURRENT_RELEASE_DIRECTORY = f"{HOME}/release-current"

ENV = {"DJANGO_SETTINGS_MODULE": "notcms.settings.prod"}


def get_remote():
    return Connection(HOST)


def get_timestamp():
    return int(datetime.now().timestamp())


@contextmanager
def virtualenv(c):
    with c.prefix(f"source .venv/bin/activate"):
        yield


@contextmanager
def npm(c):
    with c.prefix(f'export NVM_DIR="/home/{USER}/.nvm"'):
        with c.prefix(f'source "$NVM_DIR/nvm.sh"'):
            yield


@task
def git_pull(c):
    print("Pulling from latest master")
    c.run("git pull")


@task
def git_clone(c):
    print("Cloning repository")
    c.run(
        "git clone --depth 1 --branch master git@github.com:bozbalci/bozbalci-blog.git ."
    )


@task
def create_virtualenv(c):
    print("Creating virtual environment")
    c.run("python3 -m venv .venv")


@task
def inject_secrets(c):
    print("Injecting secrets")
    c.run(f"mv {HOME}/secrets/prod.env .env")


@task
def install_node_dependencies(c):
    with npm(c):
        print("Installing Node dependencies...")
        c.run("npm install")


@task
def build_frontend(c):
    with npm(c):
        print("Building frontend...")
        c.run("npm run build")


@task
def install_python_dependencies(c):
    with virtualenv(c):
        print("Installing Python dependencies...")
        c.run("pip install -r requirements.txt")


@task
def django_collectstatic(c):
    with virtualenv(c):
        print("Collecting static assets...")
        c.run("rm -vrf staticfiles/")
        c.run("python manage.py collectstatic", env=ENV, pty=True)


@task
def django_migrate_db(c):
    with virtualenv(c):
        print("Running database migrations...")
        c.run("python manage.py migrate", env=ENV)


@task
def restart_wsgi(c):
    print("Restarting WSGI server")
    c.run("sudo systemctl restart gunicorn", pty=True)


@task
def deploy_incremental(c, dependencies=True, collectstatic=True, migrate=True):
    with get_remote() as conn:
        with conn.cd(CURRENT_RELEASE_DIRECTORY):
            git_pull(conn)
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
def deploy(c):
    with get_remote() as conn:
        current_ts = get_timestamp()
        release_directory = f"{HOME}/release-{current_ts}"
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
        # conn.run(f"ln -sf {release_directory} {CURRENT_RELEASE_DIRECTORY}")


@task
def shell(c):
    with get_remote() as conn:
        with virtualenv(conn):
            conn.run(
                "python manage.py shell",
                env=ENV,
                pty=True,
            )
