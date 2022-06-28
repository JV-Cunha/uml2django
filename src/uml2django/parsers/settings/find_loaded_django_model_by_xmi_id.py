
from uml2django import  settings
from uml2django import _logger
from uml2django.objects import DjangoModel


def find_loaded_django_model_by_xmi_id(xmi_id : str) -> DjangoModel:
    found_model = None
    for model in settings.DJANGO_MODELS:
        if model.xmi_id == xmi_id:
            _logger.debug(f"Found {model} with xmi_id {xmi_id}")
            found_model = model
    if not found_model:
        _logger.debug(f"Did Not Found any model with xmi_id {xmi_id}")
    return found_model
