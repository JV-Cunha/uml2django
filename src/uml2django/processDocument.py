

import sys
import subprocess
from typing import List
from xml.dom import minidom
from uml2django.logger import _logger
from uml2django.XmiArgoUmlTagsName import XMI_ARGO_CLASS_TAG_NAME


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
    
    return "examples/MyProject.xmi"

def getClassElementsFromDocument(document: minidom.Document) -> List[minidom.Element]:
    """Get all class tags from the document

    :param document: the minidom.Document object instance
    :type document: minidom.Document
    :return: A list of minidom.Element objects
    :rtype: List[minidom.Element]
    """    
    return document.documentElement.getElementsByTagName(
        XMI_ARGO_CLASS_TAG_NAME
    )

def getAppsNamesFromDocument(document: minidom.Document) -> List[str]:
    """Get apps names defined in the XMI document.
    Assures that all models definition belongs to an app

    :param document: _description_
    :type document: minidom.Document
    :return: _description_
    :rtype: List[str]
    """    
    apps_names = []
    for class_element in getClassElementsFromDocument(document):
        if class_element.attributes.get("name") is not None:
            try:
                # All classes definitions must belongs to an app
                app_name = class_element.attributes.get("namespace").value
                if app_name not in apps_names:
                    apps_names.append(app_name)
                    _logger.info(f"Found one app: {app_name}")
            except AttributeError:
                _logger.info(
                    "Models must belongs to an app, use plant uml packages"
                )
                sys.exit(1)

    return apps_names
