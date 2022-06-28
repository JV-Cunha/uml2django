from redbaron import RedBaron
from uml2django import _logger
from uml2django.parsers.files.file_reader import file_reader



def file_writer(file_path: str, content: str, override=True):
    mode = "w" if override else "a"
    with open(file_path, mode) as file:
        file.write(str(content))
        file.close()
