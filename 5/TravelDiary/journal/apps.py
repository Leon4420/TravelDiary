"""Конфигурация приложения."""

from django.apps import AppConfig


class JournalConfig(AppConfig):
    """Определяет параметры приложения дневника путешествий."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "journal"
