import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '+z_g&xdw+d(q^z(q57v_h-3k!_3m@8cc5+=y3$@4tly(^)&8-0'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'generation',
    'djcelery',
    'kombu.transport.django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'primes.urls'

WSGI_APPLICATION = 'primes.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'media/templates'),
)


# Celery settings
BROKER_URL = 'django://'

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'generation-controller-every-30-secs': {
        'task': 'generation.tasks.controller',
        'schedule': timedelta(seconds=10),
    },
}

CELERY_TIMEZONE = 'UTC'

CELERY_TRACK_STARTED = True