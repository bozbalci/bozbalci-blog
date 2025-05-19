# Deploying to production

This project provides a `docker-compose.production.yml` for easy deployment to production environments.

FYI: My production setup has a dedicated managed Postgres instance, so it's not included in the docker compose.


## First deployment

1. Provision a Linux server and complete initial setup.
   - I followed this guide: [Initial Server Setup with Ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu)
2. Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
3. Clone the repository:
   ```shell
   $ git clone git@github.com:bozbalci/bozbalci-blog.git
   ```
4. Place production secrets into `.envs/.production/`
   - If you set up `fab` locally, and if you have the `.production` directory locally, then you can run `fab push-prod-envfiles`.
5. Build the stack:
   ```shell
   $ docker compose -f docker-compose.production.yml build
   ```
6. Run it:
   ```shell
   $ docker compose -f docker-compose.production.yml up -d
   ```

If you need to run database migrations, you can either run them on the server using the following command:

```shell
$ docker compose -f docker-compose.production.yml run --rm django python manage.py migrate
```

or from your machine using `fab migrate`.

### Surviving reboots

See: [https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html#example-supervisor](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html#example-supervisor)

This project is provided with a Supervisor config.

```shell
$ sudo apt install supervisor
$ sudo cp compose/production/supervisord.conf /etc/supervisor/conf.d/notcms.conf
$ sudo supervisorctl reread
$ sudo supervisorctl update
$ sudo supervisorctl start notcms
# For status check:
$ sudo supervisorctl status
```

## Subsequent deployments

This project is configured to automatically deploy from GitHub actions, assuming you've added the following secrets:

- SSH_HOST
- SSH_USER
- SSH_KEY
