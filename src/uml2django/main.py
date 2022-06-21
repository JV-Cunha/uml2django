"""
Main file.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""
import os
import sys
from typing import List
from uml2django import _logger, settings
from uml2django.processDocument import (
    read_xmi_file,
    generate_xmi_from_puml,
    start_django_project,
)
from uml2django.argparser import parse_args
from uml2django.processDocument.DjangoModel import DjangoModel
from uml2django.processDocument import get_django_models_from_minidom_document

__author__ = "Joao Victor Soares da Cunha"
__copyright__ = "Joao Victor Soares da Cunha"
__license__ = "MIT"


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.
def main(args: List[str]):
    args = parse_args(args)
    if settings.UML2DJANGO_GENERATE_DJANGO_PROJECT:
        start_django_project()
    
    for django_model in settings.DJANGO_MODELS:
        django_model.generate_model_python_file()
        if not django_model.is_abstract:
            django_model.generate_rest_api()
            django_model.generate_model_forms()
            django_model.generate_class_based_views()
            django_model.generate_cbv_urls_routing()
            django_model.generate_templates()
    sys.exit(1)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html
    run()
