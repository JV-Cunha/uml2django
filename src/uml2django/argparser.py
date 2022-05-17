import os
import argparse
import logging
from uml2django import __version__
from typing import List
from uml2django import config



def is_valid_file(parser: argparse.ArgumentParser, arg: str) -> str:
    """Checks that filename given as argument is valid

    Args:
        parser (argparse.ArgumentParser): The ArgumentParser instance
        arg (str): The filename given as argument

    Returns:
        str: The filename given as argument
    """

    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def is_valid_directory(parser: argparse.ArgumentParser, path: str):
    if os.path.isdir(path):
        return path
    else:
        parser.error("The directory %s does not exist!" % path)


def parse_args(args : List[str]) -> argparse.Namespace:
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

    parser.add_argument('--xmi',
                        dest="xmi_file", metavar="FILE",
                        help="path to XMI file",
                        type=lambda arg: is_valid_file(parser, arg))

    parser.add_argument('--puml',
                        dest="puml_file", metavar="FILE",
                        help="path to PlantUml file",
                        type=lambda arg: is_valid_file(parser, arg))

    parser.add_argument('-o', '--out',
                        dest="output_path", metavar="PATH",
                        help="output path for generated code",
                        type=lambda arg: is_valid_directory(parser, arg))
    parser.add_argument(
        "--version",
        action="version",
        version="uml2django {ver}".format(ver=__version__),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parsed_args = parser.parse_args(args)
    if not (parsed_args.xmi_file or parsed_args.puml_file):
        parser.error('No file given, add --xmi or --puml')
    
    if parsed_args.output_path:
        config.OUTPUT_PATH = parsed_args.output_path
        print(config.OUTPUT_PATH)
    return parsed_args
