import os
from Cheetah.Template import Template
from uml2django import settings, templates

from uml2django.processDocument.file_writer import file_writer


def generate_prepare_database():
    prepare_database_template = Template(
        file=templates.PREPARE_DATABASE
    )
    file_writer(
        file_path=os.path.join(
            settings.UML2DJANGO_OUTPUT_PATH, "prepare_database.py"
        ),
        content=(str(prepare_database_template))
    )