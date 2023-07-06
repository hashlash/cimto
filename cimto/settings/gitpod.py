import subprocess
from urllib.parse import urlparse

from .development import *  # noqa

GITPOD_SERVICE_URL = urlparse(subprocess.getoutput('gp url 8000'))

ALLOWED_HOSTS = [GITPOD_SERVICE_URL.hostname]
CSRF_TRUSTED_ORIGINS = [GITPOD_SERVICE_URL.geturl()]
