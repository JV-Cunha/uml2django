import os
import sys
from xml.dom import minidom
from Cheetah.Template import Template
import inflect
from uml2django import templates
from uml2django import config
from uml2django.XmiArgoUmlTagsName import (
    XMI_ARGO_ATTRIBUTE_TAG_NAME,
    XMI_ARGO_CLASS_TAG_NAME
)
from uml2django.logger import _logger
from pathlib import Path

from uml2django.processDocument.DjangoModelField import DjangoModelField

class DjangoModel():
    element = None
    xmi_id = None
    app_name = str()
    name = str()
    fields = list()
    views_path = str()
    actions = [
        'create', 'delete', 'detail',
        'list', 'update',
    ]

    @classmethod
    def generateCodeFromDocument(cls, document: minidom.Document) -> list:
        for model in cls.getFromDocument(document):
            model.generate_model_python_file()
            model.generate_model_form()
            model.generate_class_based_views()
            model.generate_templates()
        return None

    def generate_model_form(self):
        Path(self.app_forms_path).mkdir(parents=True, exist_ok=True)
        t = Template(file=templates.MODEL_FORM_TEMPLATE_PATH)
        t.model = self
        model_form_file_path = os.path.join(
            self.app_forms_path, f"{self.name}ModelForm.py"
        )
        # write model form file
        with open(model_form_file_path, "w") as text_file:
            text_file.write(str(t))
            text_file.close()
        # add import to __init__.py
        with open(self.app_forms_init_path, "a") as text_file:
                text_file.write(f"from .{self.name}ModelForm import {self.name}ModelForm\n")
                text_file.close()

    def generate_templates(self):
        Path(self.app_templates_path).mkdir(parents=True, exist_ok=True)
        for action in self.actions:
            cap_action = action.capitalize()
            t = Template(
                file=templates.getTemplatePath(
                    directory="templates",
                    filename=f"template_{action}.tmpl"
                )
            )
            t.model = self
            template_file_path = os.path.join(
                self.app_templates_path, f"{self.name}_{cap_action}.html"
            )
            with open(template_file_path, "w") as template_file:
                template_file.write(str(t))
                template_file.close()
                
                
    def generate_class_based_views(self):
        views = self.actions
        Path(self.model_views_path).mkdir(parents=True, exist_ok=True)
        for view_name in views:
            cap_view_name = view_name.capitalize()
            t = Template(
                file=templates.getTemplatePath(
                    directory="views",
                    filename=f"{cap_view_name}View.tmpl"
                )
            )
            t.model = self
            view_file_path = os.path.join(
                self.model_views_path, f"{self.name}{cap_view_name}View.py"
            )
            with open(view_file_path, "w") as view_file:
                view_file.write(str(t))
                view_file.close()
            # add import to __init__.py inside model views path
            with open(self.model_views_init_file_path, "a") as model_views_init_file:
                model_views_init_file.write(f"from .{self.name}{cap_view_name}View import {self.name}{cap_view_name}View\n")
                model_views_init_file.close()
            # add import to __init__.py inside app views path
            with open(self.app_views_init_file_path, "a") as app_views_init_file:
                app_views_init_file.write(f"from .{self.name} import {self.name}{cap_view_name}View\n")
                app_views_init_file.close()

    @classmethod
    def getFromDocument(cls, document: minidom.Document) -> list:
        """Get the xmi classes that have its name attribute setted
        Classes whitout name are used to represent association,
        they have xmi_id attribute setted instead

        :param document: the minidom.Document object instance
        :type document: minidom.Document
        :return: The List with classes elements
        :rtype: List[minidom.Element]
        """
        django_models = []
        class_elements = document.documentElement.getElementsByTagName(
            XMI_ARGO_CLASS_TAG_NAME
        )
        
        for class_element in class_elements:
            if class_element.attributes.get("name") is not None:
                django_models.append(DjangoModel(class_element))
        return django_models

    def __init__(self, element: minidom.Element = None):
        if not element:
            _logger.debug("An element must be given")
            sys.exit(1)
        self.element = element
        self.setNamesFromElement()
        self.app_name = element.attributes.get("namespace").value
        self.setFieldsFromElement()
        self.setPaths()

    def generate_model_python_file(self):
        model = self
        t = Template(file=templates.MODEL_TEMPLATE_PATH)
        t.model = self
        Path(self.app_models_path).mkdir(parents=True, exist_ok=True)
        model_file_path = os.path.join(self.app_models_path, f"{model.name}.py")
        # write model file
        with open(model_file_path, "w") as text_file:
            text_file.write(str(t))
            text_file.close()
        # add import to __init__.py
        with open(self.app_models_init_path, "a") as text_file:
            text_file.write(f"from .{self.name} import {self.name}\n")
            text_file.close()
    
    def setNamesFromElement(self):
        self.name = self.element.attributes.get("name").value.lower().capitalize()
        self.name_lower = self.name.lower()
        self.name_plural = inflect.engine().plural(self.name)
        return self.name
    
    def setFieldsFromElement(self):
        attributes_elements = self.element.getElementsByTagName(
            XMI_ARGO_ATTRIBUTE_TAG_NAME
        )
        attributes = list(
            map(
                lambda element: DjangoModelField(element), attributes_elements
                )
            )
        self.fields = attributes

    def setPaths(self):
        # App path
        self.app_path = os.path.join(
            config.OUTPUT_PATH,
            self.app_name,
        )
        # Models path
        self.app_models_path = os.path.join(
            config.OUTPUT_PATH,
            self.app_name,
            "models"
        )
        # Models __init__.py path
        self.app_models_init_path = os.path.join(
            self.app_models_path,
            "__init__.py"
        )
        # App Forms path
        self.app_forms_path = os.path.join(
            self.app_path,
            "forms",
        )
        # App Forms __init__.py path
        self.app_forms_init_path = os.path.join(
            self.app_path,
            "forms",
            "__init__.py"
        )
        # App Views path
        # example: some_django_app/views/
        self.app_views_path = os.path.join(
            self.app_path,
            "views",
        )
        # App Views Path
        # example: some_django_app/views/__init__.py
        self.app_views_init_file_path = os.path.join(
            self.app_views_path,
            "__init__.py"
        )
        # Model Views Path
        # example: some_django_app/views/some_model/ 
        self.model_views_path = os.path.join(
            self.app_views_path,
            self.name,
        )
        # Model Views __init__ Path
        # example: some_django_app/views/some_model/__init__.py
        self.model_views_init_file_path = os.path.join(
            self.model_views_path, "__init__.py"
        )
        # App Templates paths
        # example: some_django_app/templates/
        self.app_templates_path = os.path.join(
            self.app_path,
            "templates",
        )
        self.model_templates_path = os.path.join(
            self.app_templates_path,
            self.name,
        )
