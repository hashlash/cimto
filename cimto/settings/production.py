import os

import dj_database_url

from .base import *  # noqa

ALLOWED_HOSTS = ['cimto.fly.dev']

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config()  # noqa: F405
