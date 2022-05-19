import os

import sys
import subprocess
from xml.dom import minidom


def prepend_to_file(file_path, content):
    """ Add content to begin of the file  """
    file = open(file_path, 'r+', encoding='utf-8')
    lines = file.readlines()
    file.seek(0)
    file.write(content)
    for line in lines:  # write old content after new
        file.write(line)
    file.close


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
