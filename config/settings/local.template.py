import sys
import socket

from .common import *
from .common.dev_tools import *

FRONTEND_URL = ''
ENVIRONMENT = "local"
DEBUG = True

# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False

INTERNAL_IPS = (
    "0.0.0.0",
    "127.0.0.1",
)
# Hack to have working `debug` context processor when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += (ip[:-1] + "1",)

DATABASES = dict(
    default=dict(
        ENGINE="django.db.backends.postgresql",
        NAME="rent-checker-dev",
        USER="rent-checker-user",
        PASSWORD="manager",
        HOST="postgres",
        PORT="5432",
        ATOMIC_REQUESTS=True,
        CONN_MAX_AGE=600,
    ),
)

# Don"t use celery when you"re local
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_ROUTES = {}
CELERY_BROKER_URL = "redis://redis/1"
CELERY_RESULT_BACKEND = "redis://redis/1"
CELERY_TASK_DEFAULT_QUEUE = "development"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_EMAIL_VERIFICATION = "none"

# disable any password restrictions
AUTH_PASSWORD_VALIDATORS = []

CACHES = dict(
    default=dict(
        BACKEND="django_redis.cache.RedisCache",
        LOCATION="redis://redis/1",
        OPTIONS=dict(
            CLIENT_CLASS="django_redis.client.DefaultClient",
            MAX_ENTRIES=1000
        ),
    ),
)
