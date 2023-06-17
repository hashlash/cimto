import os

import dj_database_url

from .base import *  # noqa

ALLOWED_HOSTS = ['cimto.fly.dev']

CSRF_TRUSTED_ORIGINS = ['https://cimto.fly.dev']

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config()  # noqa: F405


# Whitenoise setting
# https://whitenoise.readthedocs.io/en/latest/

# put whitenoise after security middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa: F405
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
