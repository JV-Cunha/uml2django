import os
from Cheetah.Template import Template
from uml2django import objects, templates
from uml2django.settings import settings

from uml2django.parsers.files.file_writer import file_writer


def generate_prepare_database():
    prepare_database_template = Template(
        file=templates.PREPARE_DATABASE
    )
    prepare_database_template.models = objects.DJANGO_MODELS
    prepare_database_template.project_name = settings.UML2DJANGO_PROJECT_NAME
    file_writer(
        file_path=os.path.join(
            settings.UML2DJANGO_OUTPUT_PATH, "prepare_database.py"
        ),
        content=(str(prepare_database_template))
    )
