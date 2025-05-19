import sys
from contextlib import contextmanager
from pathlib import Path

import environ
from colorama import Fore, Style
from fabric import Connection, task

BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

SSH_HOST = env("FABRIC_SSH_HOST")
SSH_USER = env("FABRIC_SSH_USER")
GITHUB_REPO = env("FABRIC_GITHUB_REPO")
PROJECT_NAME = env("FABRIC_PROJECT_NAME", default=GITHUB_REPO.split("/")[1])


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


class Remote:
    def __init__(self, *, connection=None):
        if connection is None:
            connection = Connection(SSH_HOST)
        self.conn = connection

    @contextmanager
    def project_root(self):
        with self.conn.cd(PROJECT_NAME):
            yield

    def _compose(self, command):
        return self.conn.run(
            f"docker compose -f docker-compose.production.yml {command}"
        )

    def django_migrate(self):
        info("Migrating production Django database...")
        with self.project_root():
            self._compose("run --rm django python manage.py migrate")

    def django_create_superuser(self):
        info("Creating Django superuser...")
        with self.project_root():
            self._compose("run --rm django python manage.py createsuperuser")

    def django_shell(self):
        info("Launching production Django shell...")
        with self.project_root():
            self._compose("run --rm django python manage.py shell")

    def view_logs(self, service=None):
        info("Viewing production logs...")
        service_flag = f"{service}" if service else ""
        with self.project_root():
            self._compose(f"logs {service_flag}")

    def ps(self):
        with self.project_root():
            self._compose("ps")


@task
def migrate(c):
    Remote().django_migrate()


@task
def createsuperuser(c):
    Remote().django_create_superuser()


@task
def shell(c):
    Remote().django_shell()


@task
def logs(c, service: str | None = None):
    Remote().view_logs(service)


@task
def ps(c):
    Remote().ps()
