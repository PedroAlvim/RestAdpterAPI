from pathlib import Path

import django
from django.conf import settings

from API.person_api.apps import PersonApiConfig

PersonApiConfig.name = 'API.person_api'

BASE_DIR = Path(__file__).resolve().parent.parent

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'API/db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'API.person_api',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    SECRET_KEY='django-insecure-j9qa9)vxraj0lbi6r3*3mi@)u-w$g=#0#xkl7l2wd#h@c(oq@('
)
django.setup()

from API.person_api.models import University