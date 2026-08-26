"""Настройка ASGI для проекта TravelDiary."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traveldiary.settings")
application = get_asgi_application()
