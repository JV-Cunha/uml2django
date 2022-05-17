# Generate by uml2django 

import os
from uml2django import templates


def getTemplatePath(filename: str) -> str:
    path = os.path.dirname(templates.__file__)
    template_path = os.path.join(path, filename)
    return template_path

def getViewsTemplatePath(filename: str) -> str:
    path = os.path.dirname(templates.__file__)
    template_path = os.path.join(path, "views", filename)
    return template_path


BASE_MODEL_TEMPLATE_PATH = getTemplatePath("base_model.tmpl")
MODEL_TEMPLATE_PATH = getTemplatePath("model.tmpl")

CREATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("create.tmpl")
DELETE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("delete.tmpl")
DETAIL_VIEW_TEMPLATE_PATH = getViewsTemplatePath("detail.tmpl")
LIST_VIEW_TEMPLATE_PATH = getViewsTemplatePath("list.tmpl")
UPDATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("update.tmpl")
