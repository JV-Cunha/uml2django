from uml2django.settings import settings
from uml2django import objects
from uml2django.parsers.xmi.generate_xmi_from_puml import generate_xmi_from_puml
from uml2django.parsers.xmi.get_django_models_from_xmi_document import get_django_models_from_xmi_document
from uml2django.parsers.xmi.load_associations import load_associations
from uml2django.parsers.xmi.read_xmi_file import read_xmi_file


def load_data_from_puml_or_xmi(xmi_file_path: str = "", plantuml_file_path: str = ""):
    if not xmi_file_path and not plantuml_file_path:
        raise AttributeError("Shoud contain at least one parameter")

    xmi_filename = xmi_file_path
    if not xmi_file_path:
        xmi_filename = generate_xmi_from_puml(plantuml_file_path)
    settings.UML2DJANGO_PROJECT_NAME = xmi_filename[:-4].split("/")[-1]
    settings.DOCUMENT_OBJECT_MODEL = read_xmi_file(xmi_filename)
    objects.DJANGO_MODELS = get_django_models_from_xmi_document(
        settings.DOCUMENT_OBJECT_MODEL
    )
    objects.DJANGO_MODELS_NAMES = [
        model.name for model in objects.DJANGO_MODELS]
    for django_model in objects.DJANGO_MODELS:
        django_model.process_operations()
    load_associations()
    return True