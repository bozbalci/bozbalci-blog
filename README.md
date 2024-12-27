# not a cms

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Welcome to the source code for my blog!

## Running

```bash
# Start the Django development server:
$ source ~/.venvs/not-cms/bin/activate
(not-cms) $ export=DJANGO_SETTINGS_MODULE=notcms.settings.dev
(not-cms) $ python manage.py collectstatic
(not-cms) $ python manage.py runserver &
# Start the Vite development server:
(not-cms) $ npm run dev
```