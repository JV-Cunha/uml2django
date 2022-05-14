import os
import argparse
import logging
from uml2django import __version__
from typing import List

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg
    
def parse_args(args : List[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")

    parser.add_argument('--xmi_file',
                        dest="xmi_file", metavar="FILE",
                        help="path to XMI file",
                        type=lambda x: is_valid_file(parser, x))

    parser.add_argument('--puml_file',
                        dest="puml_file", metavar="FILE",
                        help="path to PlantUml file",
                        type=lambda x: is_valid_file(parser, x))

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
        parser.error('No file given, add --xmi_file or -puml_file')

    return parsed_args
