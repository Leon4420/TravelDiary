"""Настройка WSGI для проекта TravelDiary."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traveldiary.settings")
application = get_wsgi_application()
