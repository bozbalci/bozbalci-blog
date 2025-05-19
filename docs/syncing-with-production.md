# Syncing with production

## Sync database (non-Docker)

```sh
$ fab sync-with-prod-db
```

## Sync database (Docker)

TODO: There should be a nicer way to do this

```sh
# (Obtain a SQL dump)
$ pg_dump -U user -h host dbname > dump.sql
# Locally:
$ cat dump.sql | docker exec -i notcms_local_postgres psql -U postgres_user -d postgres_db
```

## Sync AWS S3 media

```sh
$ aws s3 sync s3://i.bozbalci.me media
```
