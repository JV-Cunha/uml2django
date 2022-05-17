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
            model.generateModelPythonFile()
            model.generateClassBasedViews()
            model.generateTemplates()
        return None

    def generateTemplates(self):
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
                
                
    def generateClassBasedViews(self):
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
        """Get and return the classes that have its name attribute setted
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
        
        

    def generateModelPythonFile(self):
        model = self
        t = Template(file=templates.MODEL_TEMPLATE_PATH)
        t.model = self
        app_models_path = os.path.join(
            config.OUTPUT_PATH,
            f"{model.app_name}",
            "models"
        )

        Path(app_models_path).mkdir(parents=True, exist_ok=True)
        init_file_path = os.path.join(app_models_path, "__init__.py")
        model_file_path = os.path.join(app_models_path, f"{model.name}.py")
        # write model file
        with open(model_file_path, "w") as text_file:
            text_file.write(str(t))
            text_file.close()
        # add import to __init__.py
        with open(init_file_path, "a") as text_file:
                text_file.write(f"from .{model.name} import {model.name}\n")
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
        self.app_path = os.path.join(
            config.OUTPUT_PATH,
            self.app_name,
        )
        self.app_views_path = os.path.join(
            self.app_path,
            "views",
        )
        self.app_views_init_file_path = os.path.join(
            self.app_views_path,
            "__init__.py"
        )
        self.model_views_path = os.path.join(
            self.app_views_path,
            self.name,
        )
        self.model_views_init_file_path = os.path.join(
            self.model_views_path, "__init__.py"
        )
        
        self.app_templates_path = os.path.join(
            self.app_path,
            "templates",
        )
        self.model_templates_path = os.path.join(
            self.app_templates_path,
            self.name,
        )
