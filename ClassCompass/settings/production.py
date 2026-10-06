from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'lrangu2.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}