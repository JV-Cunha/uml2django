import os
from uml2django import templates


def getTemplatePath(filename: str,directory = "") -> str:
    current_path = os.path.dirname(templates.__file__)
    cheetah_templates_path = os.path.join(current_path, "templates")
    template_path = os.path.join(cheetah_templates_path, directory, filename)
    return template_path

def getViewsTemplatePath(filename: str) -> str:
    return getTemplatePath(filename, "views")



BASE_MODEL_TEMPLATE_PATH = getTemplatePath("BaseModel.tmpl", "models")
MODEL_TEMPLATE_PATH = getTemplatePath("Model.tmpl", "models")
MODEL_CREATE_FORM_TEMPLATE_PATH = getTemplatePath("ModelCreateForm.tmpl", "forms")
MODEL_UPDATE_FORM_TEMPLATE_PATH = getTemplatePath("ModelUpdateForm.tmpl", "forms")

CREATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("CreateView.tmpl")
DELETE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("DeleteView.tmpl")
DETAIL_VIEW_TEMPLATE_PATH = getViewsTemplatePath("DetailView.tmpl")
LIST_VIEW_TEMPLATE_PATH = getViewsTemplatePath("ListView.tmpl")
UPDATE_VIEW_TEMPLATE_PATH = getViewsTemplatePath("UpdateView.tmpl")