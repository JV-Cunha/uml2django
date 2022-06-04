"""
Main file.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import sys
from typing import List
from uml2django.processDocument import (
    readXmiFile,
    generateXmiFromPuml,
)
from uml2django.logger import setup_logging
from uml2django.argparser import parse_args
from uml2django.processDocument.DjangoModel import DjangoModel

__author__ = "Joao Victor Soares da Cunha"
__copyright__ = "Joao Victor Soares da Cunha"
__license__ = "MIT"


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.
def main(args: List[str]):
    args = parse_args(args)
    setup_logging(args.loglevel)

    if args.xmi_file is None:
        xmi_filename = generateXmiFromPuml(args.puml_file)
    document_object_model = readXmiFile(xmi_filename)
    project_name = args.xmi_file[:-5]
    # apps_names = getAppsNamesFromDocument(document_object_model)
    models = DjangoModel.generateCodeFromDocument(document_object_model)

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
