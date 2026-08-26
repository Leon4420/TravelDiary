"""Утилита командной строки для административных задач Django."""

import os
import sys


def main():
    """Запускает выполнение административных команд."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traveldiary.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
