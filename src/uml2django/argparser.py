import os
import argparse
import logging
from typing import List
from pathlib import Path

from uml2django import __version__
from uml2django import settings
from uml2django.processDocument import generate_xmi_from_puml, read_xmi_file


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
    # XMI file or PUML file MUST be inform
    if not (parsed_args.xmi_file or parsed_args.puml_file):
        parser.error('No file given, add --xmi or --puml')

    # XMI file or PUML file MUST be inform, NOT BOTH
    if (parsed_args.xmi_file and parsed_args.puml_file):
        parser.error('You should inform --xmi or --puml')
    
    if parsed_args.xmi_file is None:
        xmi_filename = generate_xmi_from_puml(parsed_args.puml_file)
    settings.DOCUMENT_OBJECT_MODEL = read_xmi_file(xmi_filename)

    # Configure Output Path
    # Create path if not exists
    if parsed_args.output_path:
        settings.UML2DJANGO_OUTPUT_PATH = parsed_args.output_path
        if not os.path.exists(settings.UML2DJANGO_OUTPUT_PATH):
            Path(settings.UML2DJANGO_OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
        else:
            if os.path.isfile(settings.UML2DJANGO_OUTPUT_PATH):
                parser.error('Output directory path exists and is a file ')
    
    # if parse_args.clean:
                

    return parsed_args
