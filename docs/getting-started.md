# Getting started with "not-a-cms"

This application was tested on the following setup:

- Python 3.12
- node v23.4.0
- npm 10.9.2
- PostgreSQL 14.15

## Database setup

In order to run this application locally, you need to set up a Postgres database
server.

Here are the instructions for macOS:

```shell
$ brew install postgresql
$ brew services start postgresql
```

You can verify that Postgres is running by running `pg_isready`.

Launch a Postgres shell by running `psql postgres` on the shell, and then run
the following commands:

```sql
CREATE USER django_notcms_owner WITH PASSWORD 'password';
ALTER ROLE django_notcms_owner SET client_encoding TO 'utf8';
ALTER ROLE django_notcms_owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_notcms_owner SET timezone to 'UTC';
CREATE DATABASE notcms OWNER django_notcms_owner;
```

This should set up the permissions correctly, but if you run into any permission
issues down the line, I've found the following commands helped:

```sql
GRANT ALL PRIVILEGES ON DATABASE notcms TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_notcms_owner;
GRANT USAGE ON SCHEMA public TO django_notcms_owner;
GRANT CREATE ON SCHEMA public TO django_notcms_owner;
```

## Preparing the environment

Create a `.env` file at the project root. You need the following keys:

```dotenv
# Postgres
POSTGRES_HOST="localhost"
POSTGRES_PORT=""
POSTGRES_NAME="notcms"
POSTGRES_USER="django_notcms_owner"
POSTGRES_PASSWORD="password"
```

If you are interested in setting up the Last.fm integration, you will also need
the following keys:

```dotenv
# Last.fm API
LASTFM_API_KEY=
LASTFM_API_SECRET=
LASTFM_USERNAME=
```

## Dependencies

Install node dependencies and build the frontend:

```shell
$ npm install
$ npm run build
# Optionally, start the Vite development server (continue on a separate terminal)
$ npm run dev
```

Create a Python virtual environment, and activate it:

```shell
$ python --version
Python 3.12.8  # Make sure you have at least 3.12
$ python -mvenv .venv
$ source ~/.venvs/not-cms/bin/activate
```

Start the Django development server:

```shell
# This is equal to the default value, but explicit is better:
(not-cms) $ export DJANGO_SETTINGS_MODULE=notcms.settings.dev_postgres
(not-cms) $ python manage.py makemigrations
(not-cms) $ python manage.py migrate
(not-cms) $ python manage.py collectstatic
(not-cms) $ python manage.py runserver
```
