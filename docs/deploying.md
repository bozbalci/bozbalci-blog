# Deploying to production

In order to deploy this application to production, you will need the following:

- Linux server, I use a DigitalOcean droplet
- Postgres database, I use a managed DB service from DigitalOcean

You can host the database from the same machine as the web server if you wish.

I followed these tutorials to set up the production environment (minus the Postgres bits, because I'm running it separately:

- [Initial Server Setup with Ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu)
- [How To Install Node.js on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04)
- [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)

## Prerequisites

### Host machine configuration

Add the remote machine to your `.ssh/config`:

```
Host <your-remote-hostname-here>
    HostName <your-remote-ip-address-here>
```

Add your key to the authorized keys for the remote host. DigitalOcean already
takes care of this when you create the droplet.

I use `webmaster` as the username, but you don't have to.

```shell
$ ssh root@<hostname>
# At the remote root shell:
$ adduser webmaster
$ usermod -aG sudo webmaster
$ ufw allow OpenSSH
$ ufw enable
$ rsync --archive --chown=webmaster:webmaster ~/.ssh /home/webmaster
$ exit
```

Now, update your SSH config to include the username as well:

```
Host <your-remote-hostname-here>
    HostName <your-remote-ip-address-here>
    User webmaster
```

You can now directly SSH into the non-root user as follows:

```shell
# At your local:
$ ssh <hostname>
```

The remote machine needs to be able to pull code from GitHub in order to deploy,
so we will be creating an SSH key on the remote machine.

- [GitHub Docs: how to create an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)

```shell
# (at the remote machine)
$ ssh-keygen -t ed25519 -C "your_email@example.com"
# Copy the contents of ~/.ssh/id_ed25519.pub to GitHub
```

Install the required packages:

```shell
$ sudo apt update
$ sudo apt install python3-venv python3-dev nginx curl
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
$ source ~/.bashrc
$ nvm install v23.5.0
$ nvm use v23.5.0
```

Assuming that you were able to run the app locally before attempting to deploy,
you should have a `.env` file at the project root already. Amend the file to
include the following lines:

```dotenv
PROD_HOST="<hostname>"
PROD_USER="webmaster"
```

This enables [Fabric](https://www.fabfile.org) to SSH into the production server.
We can now use the `fab` command-line utility on our local machine (provided the
virtual environment is active.)

### Secrets management

Create `secrets/prod.env` at the project root on your local machine. This file
should never be checked into version control (already included in `.gitignore`).

The following values will need to be populated:

```dotenv
DJANGO_SECRET_KEY=
# If supplied, you can access the site from its remote IP address
IP_ADDRESS=

# AWS (required for S3 storage backend)
AWS_S3_REGION_NAME=
AWS_STORAGE_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_CUSTOM_DOMAIN=

# Last.fm (optional)
LASTFM_API_KEY=
LASTFM_API_SECRET=
LASTFM_USERNAME=

# Postgres (production)
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DATABASE=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

If you need to generate a secret key, you can use Django's builtin
`django.core.management.utils.get_random_secret_key` from an interactive Python
shell.

Activate your virtualenv and run `python manage.py shell`, then type:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# 12(+t_1gq$!fq5!x$32bpk=c(dw$=*ni61936p83@)a(9a9jh6
```

Once you're finished setting up `secrets/prod.env`, push the secrets to the remote:

```shell
$ fab push-secrets
```

### Provisioning

Configure systemd services and nginx (feel free to edit the configuration at `config/`)

```shell
$ fab configure-remote
```

Deploy without releasing:

```shell
$ fab deploy --no-release
```

This command will create a new directory on the remote machine, clone the
repository, create a Python virtualenv, install Node and Python dependencies,
build the frontend, run `manage.py` commands for Django, and exit.



## Incremental deployment

If you do not wish to make a clean slate deployment, a quicker version of the script can be run as follows:

```shell
$ fab deploy-incremental
```

Quicker still is the stripped version, where the deployment only pulls the repository and restarts the WSGI server:

```shell
$ fab deploy-incremental --no-collectstatic --no-dependencies --no-migrate
```
