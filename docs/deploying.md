# Deploying to production

**TL;DR – if you've already completed your first release:**

- Updated secrets? `fab push-secrets`
- Updated nginx or gunicorn conf? `fab provision`
- Deploy: `fab deploy` or `fab deploy-incremental`
- Release: `fab release`
- Rollback: `fab rollback`
- Delete deployment: `fab delete`
- Show all versions: `fab show`
- Show all available Fabric commands: `fab --list`

---

In order to deploy this application to production, you will need the following:

- Linux server, I use a DigitalOcean droplet
- Postgres database, I use a managed DB service from DigitalOcean

You can host the database from the same machine as the web server if you wish.

I followed these tutorials to set up the production environment (minus the Postgres bits, because I'm running it separately:

- [Initial Server Setup with Ubuntu](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu)
- [How To Install Node.js on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-22-04)
- [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)

---

**Table of contents**

<!-- TOC -->

- [Deploying to production](#deploying-to-production)
  - [Prerequisites](#prerequisites)
    - [Host machine configuration](#host-machine-configuration)
    - [Secrets management](#secrets-management)
  - [Provisioning](#provisioning)
  - [Deploying a new version](#deploying-a-new-version)
  - [Deploying incrementally](#deploying-incrementally)
  - [Rolling back](#rolling-back)
  - [Production shell access (firefighting mode!)](#production-shell-access-firefighting-mode)
  <!-- TOC -->

---

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
$ npm install -g pnpm
```

Assuming that you were able to run the app locally before attempting to deploy,
you should have a `.env` file at the project root already. Amend the file to
include the following lines:

```dotenv
PROD_HOST="<hostname in your ssh config>"
PROD_USER="webmaster"
DOMAIN="example.com"
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

Run `uv run manage.py shell`, then type:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# 12(+t_1gq$!fq5!x$32bpk=c(dw$=*ni61936p83@)a(9a9jh6
```

## Provisioning

Once you're finished setting up `secrets/prod.env`, push the secrets to the remote:

```shell
$ uv run fab push-secrets
```

Deploy without releasing:

```shell
$ uv run fab deploy --no-release
```

This command will create a new directory on the remote machine, clone the
repository, create a Python virtualenv, install Node and Python dependencies,
build the frontend, run `manage.py` commands for Django, and exit.

You can view the status of your remote deployments using `fab show`.

```shell
$ uv run fab show
[0, release, current] 59c39e0 release-1735776433
split documentation and reorganize some settings
```

The output shows that the last (and only) deployment is set to be the current
version once the web server is started.

In order to configure the systemd services for gunicorn and nginx, run the following:

```shell
$ uv run fab provision
```

You should run this command every time you update any of the configuration files under
`config/`.

All done! Your production server is now ready for future deployments.

## Deploying a new version

Once you've merged your new feature into master, deploy to production as follows:

```shell
$ uv run fab deploy
```

This command will prompt you for promoting the release to current. If you say
no, you can run `uv run fab release` later to complete the release. This command will
pick up the most recent deployment for promotion.

> [!Tip]
> This command always keeps at most 5 versions on the remote server.

## Deploying incrementally

If you do not wish to make a clean slate deployment, a quicker version of the script can be run as follows:

```shell
$ uv run fab deploy-incremental
```

Quicker still is the stripped version, where the deployment only pulls the repository and restarts the WSGI server:

```shell
$ uv run fab deploy-incremental --no-collectstatic --no-dependencies --no-migrate
```

> [!WARNING]
> You should generally not do this, as these releases cannot be rolled back
> if something goes wrong.

## Rolling back

You can roll back to a previous version using `fab rollback`. When no other
arguments are provided, this command will attempt to restore the **second** most
recent version. This is indicated on `fab show`:

```
$ uv run fab show

[0, release, current] 59c39e0 release-1735776433
split documentation and reorganize some settings

[1, rollback] 6a56063 release-1735757165
test draft version of atomic deployment script

[2] 6a56063 release-1735743770
test draft version of atomic deployment script

# Note that there can be multiple deployments per a single commit
```

How to interpret this output:

- The numbers (0,1,2...) on each deployment are shortcuts, you can run e.g.
  `uv run fab rollback 2` to rollback to an even earlier version.
- `release` indicates that this version is the release candidate, e.g.
  `uv run fab release` will attempt to promote this version to current.
- `rollback` indicates the rollback candidate, the target of `uv run fab rollback`.
- `current` indicates the currently served version.

## Production shell access (firefighting mode!)

You can run `uv run fab shell` to jump into a production Django shell.
