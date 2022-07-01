
import logging
from uml2django import objects
from uml2django.settings import  settings
from uml2django.objects import DjangoModel


def find_loaded_django_models_by_app_name(app_name : str) -> DjangoModel:
    models = []
    for model in objects.DJANGO_MODELS:
        if model.app_name == app_name:
            models.append(model)
    return models