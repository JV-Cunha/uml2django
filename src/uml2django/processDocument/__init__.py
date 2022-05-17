import os

import sys
import subprocess
from typing import List
from xml.dom import minidom


from uml2django.logger import _logger
from uml2django.XmiArgoUmlTagsName import XMI_ARGO_ATTRIBUTE_TAG_NAME, XMI_ARGO_CLASS_TAG_NAME
from uml2django import templates

import re
def pluralize(noun):
    if re.search('[sxz]$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[^aeiou]y$', noun):
        return re.sub('y$', 'ies', noun)
    else:
        return noun + 's'


def readXmiFile(filename: str) -> minidom.Document:
    """Try to Read XMI File from given filename

    Args:
        filename (str): _description_

    Returns:
        minidom.Document: Returns the document object model
    """    
    document_object_model = None
    # Try to read from given filename, exits if file not found
    try:
        document_object_model = minidom.parse(filename)
    except OSError as e:
        print(e)

    return document_object_model


def generateXmiFromPuml(puml_filename: str) -> str:
    """Generate the XMI file from a given PlantUml file

    :param puml_filename: _description_
    :type puml_filename: str
    :return: The name of generated XMI file
    :rtype: str
    """
    try:
        subprocess.run(["plantuml", puml_filename, "-txmi:argo"], capture_output=True)
    except OSError:
        sys.exit(1)
    return f"{puml_filename[:-4]}xmi"
