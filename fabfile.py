import os
from contextlib import contextmanager

from dotenv import load_dotenv
from fabric import Connection, task

load_dotenv()

HOST = os.getenv("PROD_HOST")
USER = os.getenv("PROD_USER")
PROJECT_DIRECTORY = f"/home/{USER}/bozbalci-blog"
VIRTUALENV_DIRECTORY = f"/home/{USER}/blog-virtualenv"
ENV = {"DJANGO_SETTINGS_MODULE": "notcms.settings.prod"}


def get_remote():
    return Connection(HOST)


@contextmanager
def virtualenv(c):
    with c.cd(PROJECT_DIRECTORY):
        with c.prefix(f"source {VIRTUALENV_DIRECTORY}/bin/activate"):
            yield


@contextmanager
def npm(c):
    with c.cd(PROJECT_DIRECTORY):
        with c.prefix(f'export NVM_DIR="/home/{USER}/.nvm"'):
            with c.prefix(f'source "$NVM_DIR/nvm.sh"'):
                yield


@task
def git_pull(c):
    with c.cd(PROJECT_DIRECTORY):
        print("Pulling from latest master")
        c.run("git pull")


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
def deploy_atomic(c):
    with get_remote() as conn:
        git_pull(conn)
        install_node_dependencies(conn)
        install_python_dependencies(conn)
        build_frontend(conn)
        django_collectstatic(conn)
        django_migrate_db(conn)

    restart_wsgi(conn)


@task
def shell(c):
    with get_remote() as conn:
        with virtualenv(conn):
            conn.run(
                "python manage.py shell",
                env=ENV,
                pty=True,
            )
