# Getting started

I recommend using Docker for local development. This project is configured to use Postgres, Redis and Celery locally.

1. [Get Docker](https://docs.docker.com/get-started/get-docker/)
2. Run `docker compose -f docker-compose.local.yml up -d`

This will launch:

- Postgres
- Redis
- Vite development server (with hot module replacement)
- Django app
- Celery (separate containers for [`celery.beat`](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) and worker)
- [Flower](https://flower.readthedocs.io/en/latest/)

Migrations are applied automatically during startup.

## Create superuser

You can run the following command to create a superuser in Django:

```shell
$ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

## Populating the database and media assets

The site can generally tolerate missing data (pages will just render empty).

By default, Wagtail CMS has an empty "Welcome to your Wagtail site!" page, so you need to go to `/cms` to create a new HomePage (and all the other special singleton pages) manually. You will also need to create all the site menus yourself.

Fortunately for me, I can dump the production DB load it directly to my database:

```sh
$ PGPASSWORD=... pg_dump -U django_notcms_owner -h .. -p ... -d notcms -Fc -f dump.pg
$ cat dump.pg | docker exec -i notcms_local_postgres pg_restore -U django_notcms_owner -d notcms
```

Again, as I have the privileges to my S3 bucket, I can pull media files so that they appear on my local development environment as well. This is purely optional:

```sh
$ aws s3 sync s3://i.bozbalci.me media
```

## Non-Docker setups

I don't really do this anymore, but if you have to, here's a short summary:

1. Install uv
2. `uv python install 3.13` and then `uv sync`
3. Install Postgres and run the following queries:
   ```postgresql
   CREATE USER postgres_user WITH PASSWORD 'postgres_password';
   ALTER ROLE postgres_user SET client_encoding TO 'utf8';
   ALTER ROLE postgres_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE postgres_user SET timezone to 'UTC';
   CREATE DATABASE postgres_db OWNER postgres_user;
   
   -- Just in case, I remember I had to run these at some point
   GRANT ALL PRIVILEGES ON DATABASE postgres_db TO postgres_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres_user;
   GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres_user;
   GRANT USAGE ON SCHEMA public TO postgres_user;
   GRANT CREATE ON SCHEMA public TO postgres_user;
   ```
4. Create an `.env` file at the project root.
     - This is a good start: `cp .envs/.local/.postgres .env`
5. Install Node dependencies, I use [pnpm](https://pnpm.io/)
6. Start the Vite dev server: `pnpm run dev`
7. `uv run manage.py migrate`
8. `uv run manage.py collectstatic`
9. `uv run manage.py runserver`
10. Troubleshoot issues until done!
