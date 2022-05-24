import os
import sys
from xml.dom import minidom
from Cheetah.Template import Template
import inflect
from uml2django import templates
from uml2django import config
from uml2django.XmiArgoUmlTagsNames import (
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
    urls_imports = []
    urls_paths = []

    actions = [
        'create', 'delete', 'detail',
        'list', 'update',
    ]

    @classmethod
    def generateCodeFromDocument(cls, document: minidom.Document) -> list:
        # This dictonary is used to generate the urls.py of each app defined
        # It contais the app name as key and the urls_paths as value
        apps_and_urls_paths = {
            # app_name: urls_paths
        }

        for model in cls.getFromDocument(document):
            model.generate_model_python_file()
            model.generate_model_forms()
            model.generate_class_based_views()
            model.generate_templates()

            # if app_name is not in the dict
            if model.app_name not in apps_and_urls_paths:
                apps_and_urls_paths[model.app_name] = model.urls_paths
            # if the app name already in the dict
            # append the urls paths to the existing ones
            # else:
                # apps_and_urls_paths[model.app_name] = model.urls_paths
        print(apps_and_urls_paths[model.app_name])

        # generate the urls.py file for each app defined
        for app_name in apps_and_urls_paths:
            urls_paths = apps_and_urls_paths[app_name]

            app_urls_template = Template(
                file=templates.getTemplatePath(
                    filename="urls.tmpl"
                )
            )
            app_urls_template.urls_paths = urls_paths
            app_urls_template.app_name = app_name
            # App urls.py path
            app_urls_file_path = os.path.join(
                app_name,
                "urls.py",
            )
            with open(app_urls_file_path, "w") as app_urls_file:
                app_urls_file.write(str(app_urls_template))
                app_urls_file.close()

        return None

    def generate_model_forms(self):
        Path(self.model_forms_path).mkdir(parents=True, exist_ok=True)
        for action in ["create", "update"]:
            form_class_name = f"{self.name}{action.capitalize()}Form"
            model_form_template = None
            if action == "create":
                model_form_template = Template(file=templates.MODEL_CREATE_FORM_TEMPLATE_PATH)
            elif action == "update":
                model_form_template = Template(file=templates.MODEL_UPDATE_FORM_TEMPLATE_PATH)
            model_form_template.model = self
            model_form_file_path = os.path.join(
                self.model_forms_path, f"{form_class_name}.py"
            )
            # write model form file
            with open(model_form_file_path, "w") as text_file:
                text_file.write(str(model_form_template))
                text_file.close()
            # add import to model forms __init__.py file
            with open(self.model_forms_init_path, "a") as text_file:
                text_file.write(f"from .{form_class_name} import {form_class_name}\n")
                text_file.close()
            # add import to app forms __init__.py file
            with open(self.app_forms_init_path, "a") as text_file:
                text_file.write(f"from .{self.name_lower} import {form_class_name}\n")
                text_file.close()

    def generate_templates(self):
        Path(self.model_templates_path).mkdir(parents=True, exist_ok=True)
        for action in self.actions:
            t = Template(
                file=templates.getTemplatePath(
                    directory="templates",
                    filename=f"template_{action}.tmpl"
                )
            )
            t.model = self
            template_file_path = os.path.join(
                self.model_templates_path, f"{self.name_lower}_{action}.html"
            )
            with open(template_file_path, "w") as template_file:
                template_file.write(str(t))
                template_file.close()

    def generate_class_based_views(self):
        # Create model views directory
        Path(self.model_views_path).mkdir(parents=True, exist_ok=True)
        # loop through the actions
        for view_name in self.actions:
            cap_view_name = view_name.capitalize()
            # generate view from template for each action
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
                model_views_init_file.write(
                    f"from .{self.name}{cap_view_name}View import {self.name}{cap_view_name}View\n"
                )
                model_views_init_file.close()

            # add import to __init__.py inside app views path
            with open(self.app_views_init_file_path, "a") as app_views_init_file:
                app_views_init_file.write(
                    f"from .{self.name_lower} import {self.name}{cap_view_name}View\n"
                )
                app_views_init_file.close()

            # append view path self urls_paths list
            if view_name in ("update", "delete"):
                self.urls_paths.append((
                    f"{self.name}/<int:pk>/{view_name}",
                    f"{self.name}{cap_view_name}View",
                    f"{self.name_lower}-{view_name}"
                ))
            elif view_name == "detail":
                self.urls_paths.append((
                    f"{self.name}/<int:pk>",
                    f"{self.name}{cap_view_name}View",
                    f"{self.name_lower}-{view_name}"
                ))
            else:
                self.urls_paths.append((
                    f"{self.name}/{view_name}",
                    f"{self.name}{cap_view_name}View",
                    f"{self.name_lower}-{view_name}"
                ))

        # Generate tests
        Path(self.model_tests_path).mkdir(parents=True, exist_ok=True)
        model_views_test_template = Template(
            file=templates.getTemplatePath(
                directory="tests",
                filename=f"ModelViewsTest.tmpl"
            )
        )
        model_views_test_template.model = self
        model_views_test_template.actions = self.actions
        model_views_test_file_path = os.path.join(
            self.model_tests_path, f"{self.name}ViewsTest.py"
        )
        # Write python test file from template
        with open(model_views_test_file_path, "w") as test_file:
            test_file.write(str(model_views_test_template))
            test_file.close()
        # add import to model tests __init__.py 
        with open(self.model_tests_init_file_path, "a") as app_tests_init_file:
            app_tests_init_file.write(
                f"from .{self.name}ViewsTest import {self.name}ViewsTest\n"
            )
            app_tests_init_file.close()    
        # add import to app tests __init__.py 
        with open(self.app_tests_init_file_path, "a") as app_tests_init_file:
            app_tests_init_file.write(
                f"from .{self.name_lower} import {self.name}ViewsTest\n"
            )
            app_tests_init_file.close()

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
        t.config = config
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
            self.app_forms_path,
            "__init__.py"
        )
        # Model Forms path
        self.model_forms_path = os.path.join(
            self.app_forms_path,
            self.name_lower
        )
        # App Forms __init__.py path
        self.model_forms_init_path = os.path.join(
            self.model_forms_path,
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
            self.name_lower,
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
        # Model templates
        # example: some_django_app/templates/some_model/
        self.model_templates_path = os.path.join(
            self.app_templates_path,
            self.app_name,
        )
        # App tests path
        # example: some_django_app/tests
        self.app_tests_path = os.path.join(
            self.app_path,
            "tests",
        )
        # App tests __init__ file path
        # example: some_django_app/tests
        self.app_tests_init_file_path = os.path.join(
            self.app_tests_path,
            "__init__.py",
        )
        # Model tests path
        # example: some_django_app/tests/some_model
        self.model_tests_path = os.path.join(
            self.app_tests_path,
            self.name_lower,
        )
        # Model tests path
        # example: some_django_app/tests/some_model
        self.model_tests_init_file_path = os.path.join(
            self.model_tests_path,
            "__init__.py",
        )
