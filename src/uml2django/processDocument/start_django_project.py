import os
from django.core import management as django_management

from uml2django import settings, _logger


def start_django_project():
    django_management.call_command(
        'startproject',
        (
            f"{settings.UML2DJANGO_PROJECT_NAME}",
            f"{settings.UML2DJANGO_OUTPUT_PATH}")
    )
    _logger.debug("Created Django Project")
    settings.UML2DJANGO_OUTPUT_PATH = os.path.join(
        settings.UML2DJANGO_OUTPUT_PATH,
        settings.UML2DJANGO_PROJECT_NAME
    )
    _logger.debug(f"OUTPUT_PATH: {settings.UML2DJANGO_OUTPUT_PATH}")
