# not a cms

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome to the source code for my blog!

## Running locally

This application runs on a Postgres database. Here is how you can set up the database:

```bash
$ brew install postgresql
$ brew services start postgresql
# Verify that PostgreSQL is running:
$ pg_isready
/tmp:5432 - accepting connections
$ psql postgres
```

In the Postgres shell, type:

```postgresql
CREATE USER django_notcms_owner WITH PASSWORD 'password';
ALTER ROLE django_notcms_owner SET client_encoding TO 'utf8';
ALTER ROLE django_notcms_owner SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_notcms_owner SET timezone to 'UTC';
CREATE DATABASE notcms OWNER django_notcms_owner;
```

This should set up the permissions correctly, but if you run into any permission issues down the line, I've found the following commands helped:

```postgresql
GRANT ALL PRIVILEGES ON DATABASE notcms TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO django_notcms_owner;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_notcms_owner;
GRANT USAGE ON SCHEMA public TO django_notcms_owner;
GRANT CREATE ON SCHEMA public TO django_notcms_owner;
```

Create a `.env` file at the project root. You need the following keys:

```dotenv
# Postgres
DATABASE_HOST="localhost"
DATABASE_PORT=""
DATABASE_NAME="notcms"
DATABASE_USER="django_notcms_owner"
DATABASE_PASSWORD="password"

# The local development server uses the S3 backend
AWS_S3_REGION_NAME=
AWS_STORAGE_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Required only when SiteFeature.LAST_PLAYED is enabled
LASTFM_API_KEY=
LASTFM_API_SECRET=
LASTFM_USERNAME=

# Required only if you intend to deploy to production with Fabric
PROD_HOST=
PROD_USER=
```

You can then run the application as follows:

```bash
# Initialize your virtual environment (create if missing)
$ source ~/.venvs/not-cms/bin/activate
(not-cms) $ pip install -r requirements.txt

# Start the Django development server:
(not-cms) $ export=DJANGO_SETTINGS_MODULE=notcms.settings.dev_postgres
(not-cms) $ python manage.py makemigrations && python manage.py migrate
(not-cms) $ python manage.py collectstatic
(not-cms) $ python manage.py runserver

# On a separate terminal, start the Vite development server:
(not-cms) $ npm install
(not-cms) $ npm run dev
```

## Deploying to production

Prerequisites:

1. Add `PROD_HOST` and `PROD_USER` to `.env` at the project root.
2. Add `PROD_HOST` to your SSH configuration.

   > You must be able to ssh into `PROD_HOST` via running the command
   >
   > ```shell
   > $ ssh $PROD_HOST
   > ```
   > 
   > on your local.

3. (TODO: Instructions on how to deliver secrets to the production machine)
4. Run `fab deploy`

### Incremental deployment

If you do not wish to make a clean slate deployment, a quicker version of the script can be run as follows:

```shell
$ fab deploy-incremental
```

Quicker still is the stripped version, where the deployment only pulls the repository and restarts the WSGI server:

```shell
$ fab deploy-incremental --no-collectstatic --no-dependencies --no-migrate
```