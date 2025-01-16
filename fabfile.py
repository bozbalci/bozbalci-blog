import getpass
import os
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style
from dotenv import load_dotenv
from fabric import Config, Connection, task
from jinja2 import Environment, FileSystemLoader

load_dotenv()

HOST = os.getenv("PROD_HOST")

USER = os.getenv("PROD_USER")

DOMAIN = os.getenv("DOMAIN")

if not HOST or not USER or not DOMAIN:
    print(
        "Please set the following environment variables: PROD_HOST, PROD_USER, DOMAIN"
    )
    sys.exit(1)


HOME = f"/home/{USER}"

BASE_DIR = Path(__file__).resolve().parent

GITHUB_REPO = "bozbalci/bozbalci-blog"

DJANGO_SETTINGS_MODULE = "notcms.settings.prod"

CONFIGURATION_FILES = {
    "gunicorn.service": "/etc/systemd/system/gunicorn.service",
    "gunicorn.socket": "/etc/systemd/system/gunicorn.socket",
    "nginx.conf": f"/etc/nginx/sites-available/{DOMAIN}",
}

TEMPLATE_CONTEXT = {
    "user": USER,
    "django_settings_module": DJANGO_SETTINGS_MODULE,
    "domain": DOMAIN,
}


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


def info(message):
    print(f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")


class ConfigurationTemplateRenderer:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(BASE_DIR / "config"))
        self.context = TEMPLATE_CONTEXT

    def render(self, name):
        template = self.env.get_template(name)
        return template.render(self.context)


class Configuration:
    def __init__(self, name, renderer: ConfigurationTemplateRenderer):
        self.name = name
        self.renderer = renderer
        self._tempfile = None

    def upload_to_remote(self, remote: "Remote"):
        info(f"Uploading conf {self.name} to {remote}")
        rendered_content = self.renderer.render(self.name)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(rendered_content.encode("utf-8"))
            tmp.flush()
            remote.conn.put(tmp.name, self.name)


class Remote:
    def __init__(self, *, connection=None):
        if connection is None:
            connection = Connection(HOST)
        self.conn = connection

    @contextmanager
    def current_release_directory(self):
        with self.release_directory("release-current"):
            yield

    @contextmanager
    def release_directory(self, version, create_missing=False):
        path = f"{HOME}/{version}"
        if create_missing:
            self.conn.run(f"mkdir -p {path}")
        with self.conn.cd(path):
            yield

    @staticmethod
    def _generate_version() -> str:
        timestamp = int(datetime.now().timestamp())
        return f"release-{timestamp}"

    def _get_all_releases(self) -> list[str]:
        return self.conn.run(
            'ls -d release-* | grep -E "release-[0-9]+" | sort -r', hide=True
        ).stdout.split()

    def _get_next_release_candidate(self) -> str:
        releases = self._get_all_releases()
        return releases[0]

    def _get_current_release(self) -> str | None:
        result = self.conn.run("readlink release-current", warn=True, hide=True)

        if result.ok:
            return result.stdout.strip()
        else:
            return None

    def _uv(self, cmd):
        self.conn.run(
            f"{HOME}/.local/bin/uv {cmd}",
            env={"DJANGO_SETTINGS_MODULE": DJANGO_SETTINGS_MODULE},
            pty=True,
        )

    def _npm(self, cmd):
        with self.conn.prefix(f'export NVM_DIR="/home/{USER}/.nvm"'):  # noqa: SIM117
            with self.conn.prefix('source "$NVM_DIR/nvm.sh"'):
                self.conn.run(f"{HOME}/bin/npm {cmd}", pty=True)

    def _fetch_code_from_vcs(self, clone=False):
        info("Retrieving code from Git repository...")
        if clone:
            self.conn.run(
                f"git clone --depth 1 --branch master "
                f"git@github.com:{GITHUB_REPO}.git ."
            )
        else:
            self.conn.run("git pull")

    def _inject_secrets(self):
        info("Injecting secrets...")
        self.conn.run(f"cp {HOME}/secrets/prod.env .env")

    def _install_python_dependencies(self):
        info("Running `uv sync`...")
        self._uv("sync")

    def _install_node_dependencies(self):
        info("Running `npm install`...")
        self._npm("install")

    def _build_frontend(self):
        info("Running `npm run build`...")
        self._npm("run build")

    def _django_collectstatic(self):
        info("Collecting static files...")
        self._uv("run manage.py collectstatic")

    def _django_migrate(self):
        info("Running database migrations...")
        self._uv("run manage.py migrate")

    def _restart_wsgi_server(self):
        info("Restarting WSGI server...")
        self.conn.run("sudo systemctl restart gunicorn", pty=True)

    def _ensure_current_release_exists(self, initial_version):
        """
        The gunicorn systemd service needs to point at the release-current
        directory, so link this release if it is the only release in the
        server.
        """
        self.conn.run(
            f"[ ! -L release-current ] && ln -sfn {initial_version} release-current",
            warn=True,
        )

    def _promote_version(self, version):
        if query_yes_no(f"Promote version {version} to current?", default="no"):
            self.conn.run(f"ln -sfn {version} release-current")
            self._restart_wsgi_server()

    def _resolve_rollback_version(self, target) -> str | None:
        """
        Attempt to resolve `target` into a deployment version.

        If `target` is a number (0, 1, 2...) it corresponds to the n-th most
        recent deployment shown when `fab show` is run; where 0 is the most
        recent.

        If `target` matches the release directory naming convention (e.g.
        release-1737050756) then it specifies a deployment directly.

        If `target` is not specified, then it matches the second most recent
        deployment, provided that it exists.
        """

        releases = self._get_all_releases()

        if target in releases:
            return target
        if isinstance(target, str) and target.isdigit():
            return releases[int(target)]
        elif len(releases) > 1:
            return releases[1]
        else:
            return None

    def _get_commit_hash_of_version(self, version) -> str:
        with self.release_directory(version):
            return self.conn.run(
                "git log -1 --pretty=format:'%h'", hide=True
            ).stdout.strip()

    def _get_commit_message_of_version(self, version) -> str:
        with self.release_directory(version):
            return self.conn.run(
                "git log -1 --pretty=format:'%s'", hide=True
            ).stdout.strip()

    def _ensure_secrets_directory(self):
        info("Ensuring secrets directory exists...")
        self.conn.run("mkdir -p secrets")

    def _upload_secret(self, local_path):
        info("Uploading secrets for future releases...")
        self.conn.put(local_path, remote="secrets")

    def get_django_shell_in_current_release(self):
        info("Launching production Django shell...")
        with self.current_release_directory():
            self._uv("run manage.py shell")

    def deploy(self, release_after_complete=True):
        new_version = self._generate_version()

        info(f"Deploying new version {new_version}...")

        with self.release_directory(new_version, create_missing=True):
            self._fetch_code_from_vcs()
            self._inject_secrets()
            self._install_python_dependencies()
            self._install_node_dependencies()
            self._build_frontend()
            self._django_collectstatic()
            self._django_migrate()

        self._ensure_current_release_exists(new_version)

        if release_after_complete:
            self._promote_version(new_version)

    def deploy_incremental(
        self,
        refresh_dependencies=True,
        run_django_collectstatic=True,
        run_django_migrations=True,
    ):
        info("Upgrading the last release...")

        with self.current_release_directory():
            self._fetch_code_from_vcs()
            self._inject_secrets()

            if refresh_dependencies:
                self._install_python_dependencies()
                self._install_node_dependencies()
            if run_django_collectstatic:
                self._build_frontend()
                self._django_collectstatic()
            if run_django_migrations:
                self._django_migrate()

    def release_latest_deployment(self):
        info("Releasing the latest version...")

        new_version = self._get_next_release_candidate()
        self._promote_version(new_version)

    def rollback(self, target):
        new_version = self._resolve_rollback_version(target)

        info(f"Rolling back to previous release {new_version}...")

        if new_version:
            self._promote_version(new_version)
        else:
            print("Could not find a version to rollback to")

    def pretty_print_all_deployments(self):
        """
        Pretty-prints all deployments with details. The deployment number (0, 1, 2...)
        can be given as an argument to the `rollback` command.

        Example:
            $ fab show
            [0, release, current] c7ac9ba release-1736909243
            Merge pull request #4 from bozbalci/vue-dark-mode

            [1, rollback] a7aac79 release-1736295706
            docs: add PROD_ prefix to NGINX_SERVER_NAME

            [2] 968b036 release-1735852573
            add vertical margin space around pre blocks in typography
        """
        current_version = self._get_current_release()
        all_versions = self._get_all_releases()

        for i, version in enumerate(all_versions):
            label = [", release", ", rollback", ""][min(i, 2)]
            current_flag = (
                f", {Style.BRIGHT}current{Style.NORMAL}"
                if version == current_version
                else ""
            )
            print(
                f"{Fore.BLUE}[{i}{label}{current_flag}]{Fore.RESET} ",
                end="",
            )

            try:
                commit_hash = self._get_commit_hash_of_version(version)
                commit_message = self._get_commit_message_of_version(version)
                print(
                    f"{Fore.YELLOW}{commit_hash}{Fore.RESET} {version}"
                    f"\n{commit_message}"
                    f"\n"
                )
            except Exception as e:
                print(f"{version}: Not a git repository or error occurred: {str(e)}")

    def upload_secrets(self):
        self._upload_secret(BASE_DIR / "secrets" / "prod.env")

    def upload_configs(self):
        renderer = ConfigurationTemplateRenderer()
        configs = [Configuration(name, renderer) for name in CONFIGURATION_FILES]
        for config in configs:
            config.upload_to_remote(self)


class RemoteWithSuperuser(Remote):
    def __init__(self, *, connection=None):
        if connection is None:
            sudo_pass = getpass.getpass(f"[sudo] password for {USER}: ")
            config = Config(overrides={"sudo": {"password": sudo_pass}})
            connection = Connection(HOST, config=config)
        super().__init__(connection=connection)

    def _move_configs_under_etc(self):
        for source_path, destination_path in CONFIGURATION_FILES.items():
            self.conn.sudo(f"mv {source_path} {destination_path}", hide=True)

    def _reload_systemd_config(self):
        self.conn.sudo("systemctl daemon-reload", hide=True)

    def _enable_and_restart_gunicorn(self):
        self.conn.sudo("systemctl restart gunicorn.socket", hide=True)
        self.conn.sudo("systemctl enable gunicorn.socket", hide=True)
        self.conn.run("curl --unix-socket /run/gunicorn.sock localhost", hide=True)
        self.conn.sudo("systemctl restart gunicorn", hide=True)

    def _enable_nginx_site(self):
        self.conn.sudo(
            f"ln -sfn /etc/nginx/sites-available/{DOMAIN} /etc/nginx/sites-enabled"
        )

    def _allow_nginx_in_ufw(self):
        self.conn.sudo("ufw allow 'Nginx Full'", hide=True)

    def _enable_and_restart_nginx(self):
        self.conn.sudo("systemctl restart nginx", hide=True)
        self.conn.sudo("systemctl enable nginx", hide=True)

    def move_configs_and_reload_services(self):
        self._move_configs_under_etc()
        self._reload_systemd_config()
        self._enable_and_restart_gunicorn()
        self._enable_nginx_site()
        self._allow_nginx_in_ufw()
        self._enable_and_restart_nginx()


@task
def deploy(c, release=True):
    Remote().deploy(release_after_complete=release)


@task
def deploy_incremental(c, dependencies=True, collectstatic=True, migrate=True):
    Remote().deploy_incremental(dependencies, collectstatic, migrate)


@task
def push_secrets(c):
    Remote().upload_secrets()


@task
def provision(c):
    Remote().upload_configs()
    RemoteWithSuperuser().move_configs_and_reload_services()


@task
def release(c):
    Remote().release_latest_deployment()


@task
def rollback(c, to_version=None):
    Remote().rollback(to_version)


@task
def shell(c):
    Remote().get_django_shell_in_current_release()


@task
def show(c):
    Remote().pretty_print_all_deployments()
