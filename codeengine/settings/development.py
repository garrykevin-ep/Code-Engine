
from .base import *  # NOQA


DEBUG = True
ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = 'redis://localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}