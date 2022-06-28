import subprocess
import sys
from uml2django.parsers.files.enforce_is_valid_file import is_valid_file


def generate_xmi_from_puml(puml_filename: str) -> str:
    """Generate the XMI file from a given PlantUml file

    :param puml_filename: _description_
    :type puml_filename: str
    :return: The name of generated XMI file
    :rtype: str
    """
    is_valid_file(puml_filename)
    try:
        subprocess.run(["plantuml", puml_filename,
                        "-txmi:argo"], capture_output=True)
    except OSError:
        sys.exit(1)
    return f"{puml_filename[:-4]}xmi"
