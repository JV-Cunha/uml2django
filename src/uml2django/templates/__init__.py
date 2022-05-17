# Generate by uml2django 

import os
from uml2django import templates


def getTemplatePath(filename: str,directory = "") -> str:
    path = os.path.dirname(templates.__file__)
    template_path = os.path.join(path, directory, filename)
    return template_path

def getViewsTemplatePath(filename: str) -> str:
    return getTemplatePath(filename, "views")



BASE_MODEL_TEMPLATE_PATH = getTemplatePath("base_model.tmpl")
MODEL_TEMPLATE_PATH = getTemplatePath("model.tmpl")

CREATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("CreateView.tmpl")
DELETE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("DeleteView.tmpl")
DETAIL_VIEW_TEMPLATE_PATH = getViewsTemplatePath("DetailView.tmpl")
LIST_VIEW_TEMPLATE_PATH = getViewsTemplatePath("ListView.tmpl")
UPDATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("UpdateView.tmpl")
