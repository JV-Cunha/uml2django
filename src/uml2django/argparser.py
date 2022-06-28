import logging
import os
import argparse
import shutil
from typing import List
from pathlib import Path

from uml2django import __version__
from uml2django.settings import settings
from uml2django import _logger, setup_logging
from uml2django.parsers.xmi.XmiArgoUmlTagsNames import (
    XMI_ARGO_ASSOCIATION_TAG_NAME,
    XMI_ARGO_CLASS_TAG_NAME
)
from uml2django.parsers.files.load_data_from_puml_or_xmi import load_data_from_puml_or_xmi

from uml2django.parsers.xmi.load_associations import load_associations
from uml2django.parsers.xmi.generate_xmi_from_puml import generate_xmi_from_puml
from uml2django.parsers.xmi.get_django_models_from_xmi_document import get_django_models_from_xmi_document
from uml2django.parsers.xmi.read_xmi_file import read_xmi_file


def is_valid_file(parser: argparse.ArgumentParser, arg: str) -> str:
    """Checks that filename given as argument is a valid file

    Args:
        parser (argparse.ArgumentParser): The ArgumentParser instance
        arg (str): The filename given as argument

    Returns:
        str: The filename given as argument
    """

    if not os.path.exists(arg) and os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def is_valid_directory(parser: argparse.ArgumentParser, path: str) -> str:
    """Checks that directory name given as argument is a valid directory

    Args:
        parser (argparse.ArgumentParser): The ArgumentParser instance
        path (str): The directory name given as argument

    Returns:
        str: The directory name given as argument
    """
    if os.path.isdir(path):
        return path
    else:
        parser.error("The directory %s does not exist!" % path)


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Generate Django code from UML class diagram"
    )
    parser.set_defaults(clean=False)

    parser.add_argument('--xmi',
                        dest="xmi_file", metavar="FILE",
                        help="path to XMI file",
                        type=lambda arg: is_valid_file(parser, arg))

    parser.add_argument('--puml',
                        dest="puml_file", metavar="FILE",
                        help="path to PlantUml file",
                        type=lambda arg: is_valid_file(parser, arg))

    # Output path arg option
    parser.add_argument(
        '-o', '--out',
        dest="output_path", metavar="PATH",
        help="output path for generated code",
    )

    # Print Software Version
    parser.add_argument(
        "--version",
        action="version",
        version="uml2django {ver}".format(ver=__version__),
    )

    # Clean output files
    parser.add_argument(
        "-c",
        "--clean",
        dest="clean",
        help="clean generated files",
        action="store_true",
    )

    # Set verbose level to INFO
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    # Set verbose level to DEBUG
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parsed_args = parser.parse_args(args)
    settings.LOG_LEVEL = parsed_args.loglevel
    setup_logging(settings.LOG_LEVEL)

    # Configure Output Path
    if parsed_args.output_path:
        settings.UML2DJANGO_OUTPUT_PATH = parsed_args.output_path
    # Check if output path exists
    if os.path.isdir(settings.UML2DJANGO_OUTPUT_PATH):
        if settings.UML2DJANGO_OVERRIDE:
            logging.getLogger(__name__).debug("OVERRIDE OUTPUT")
            # remove the directory and all it's content
            shutil.rmtree(settings.UML2DJANGO_OUTPUT_PATH)
    # Create path if not exists or if exists and is a file
    if not os.path.exists(settings.UML2DJANGO_OUTPUT_PATH) or (
        os.path.exists(settings.UML2DJANGO_OUTPUT_PATH) and
        os.path.isfile(settings.UML2DJANGO_OUTPUT_PATH)
    ):
        Path(settings.UML2DJANGO_OUTPUT_PATH).mkdir(
            parents=True, exist_ok=True
        )

    # Validate XMI file and PUML file
    # XMI file or PUML file MUST be inform
    if not (parsed_args.xmi_file or parsed_args.puml_file):
        parser.error('No file given, add --xmi or --puml')
    # XMI file or PUML file MUST be inform, NOT BOTH
    if (parsed_args.xmi_file and parsed_args.puml_file):
        parser.error('You should inform --xmi or --puml')
    # if not xmi_file informed, generate from plantuml file
    load_data_from_puml_or_xmi(
        plantuml_file_path=parsed_args.puml_file,
        xmi_file_path=parsed_args.xmi_file
    )

    return parsed_args
