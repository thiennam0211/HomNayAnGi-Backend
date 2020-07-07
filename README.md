# HomNayAnGi-Backend
Author: Tran Tien Cuong

Purpose: This is a project of my graduate thesis.

Description: This  is a Server-side application of [HomNayAnGi-Mobile](https://github.com/thiennam0211/HomNayAnGi-Mobile) and [HomNayAnGi-Dashboard](https://github.com/thiennam0211/HomNayAnGi-Dashboard)

Build with: [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), [Django REST framework](https://www.django-rest-framework.org/), database is [PostgreSQL](https://www.postgresql.org/) 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install
```
Change the database configuration.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Database-name',
        'USER': 'Database-username',
        'PASSWORD': 'Database-password',
        'HOST': 'localhost',
        'PORT': 'port',
    }
}
```

## Usage

```bash
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```
