import logging
import os
import sys
import json
from xml.dom import minidom
from pathlib import Path

from Cheetah.Template import Template
from redbaron import RedBaron
import inflect


from uml2django import objects, templates
from uml2django.settings import settings
from uml2django.parsers.xmi.XmiArgoUmlTagsNames import (
    XMI_ARGO_ATTRIBUTE_TAG_NAME,
    XMI_ARGO_OPERATION_TAG_NAME,
    XMI_ARGO_STEREOTYPE_TAG_NAME
)
from uml2django.parsers.xmi.is_xmi_element_abstract import is_xmi_element_abstract
from uml2django.parsers.files.add_import_to_init_file import add_import_to_init_file
from uml2django.parsers.files.file_reader import file_reader
from uml2django.parsers.python.append_target_to_from_import import append_target_to_from_import
from uml2django.parsers.files.file_writer import file_writer

from uml2django.parsers.files.get_substring_between_parenthesis import get_sub_string_between_parenthesis

from uml2django.objects.DjangoModelField import DjangoModelField


class DjangoModel():
    element = None
    xmi_id = None
    app_name = str()
    name = str()
    base_fathers = []
    fields = list()
    views_path = str()
    urls_paths = []
    is_abstract = False
    use_slug = False
    slugify_field = ""
    unique_together_fields = []
    rest_api_writable_nested_objects = []

    actions = [
        'create', 'delete', 'detail',
        'list', 'update',
    ]

    def __init__(self, element: minidom.Element = None):
        if not element:
            logging.getLogger(__name__).debug(
                "An element must be given to construct DjangoModel object"
            )
            sys.exit(1)
        self.element = element
        self.xmi_id = element.attributes.get("xmi.id").value
        self.is_abstract = is_xmi_element_abstract(self.element)
        self.setNamesFromElement()
        self.setFieldsFromElement()
        self.setPaths()
        self.urls_paths = []
        self.base_fathers = []
        self.rest_api_writable_nested_objects = []

        # append appname if not in global apps names
        if self.app_name not in objects.UML2DJANGO_APPS_NAMES:
            objects.UML2DJANGO_APPS_NAMES.append(self.app_name)

    def __str__(self) -> str:
        return self.name

    def process_operations(self):
        operation_elements = self.element.getElementsByTagName(
            XMI_ARGO_OPERATION_TAG_NAME
        )
        operations = [str(opration_element.getAttribute("name"))
                      for opration_element in operation_elements]
        # logging.getLogger(__name__).debug(f"XMI_ARGO_STEREOTYPE_TAG_NAME: {operation_elements}")
        for operation in operations:
            # check if should use slug field
            if operation.startswith("use_slug"):
                self.use_slug = True
                self.slugify_field = get_sub_string_between_parenthesis(
                    operation)
                logging.getLogger(__name__).debug(f"USE_SLUG:: {self.use_slug}")
            # check if have unique together fields
            if operation.startswith("unique_together"):
                self.unique_together_fields = get_sub_string_between_parenthesis(
                    operation).split(",")
            if operation.startswith("rest_api_writable_nested_objects"):
                objects_list = get_sub_string_between_parenthesis(
                    operation).split(",")
                for object_name in objects_list:
                    if object_name not in objects.DJANGO_MODELS_NAMES:
                        raise AttributeError(
                            f"rest_api_writable_nested_objects: Object {object_name} not found"
                        )
                    django_model = [
                        dj_m for dj_m in objects.DJANGO_MODELS if dj_m.name == object_name]

                    if len(django_model) > 1:
                        raise AttributeError(
                            f"rest_api_writable_nested_objects: Object {object_name} is duplcated, models must have unique names"
                        )

                    self.rest_api_writable_nested_objects.append(
                        django_model[0])

    def add_base_father(self, django_model):
        self.base_fathers.append(django_model)
        logging.getLogger(__name__).debug(
            f"{str(self)} fathers: {[str(father) for father in self.base_fathers]}")

    def generate_model_forms(self):
        Path(self.model_forms_path).mkdir(parents=True, exist_ok=True)
        for action in ["create", "update"]:
            form_class_name = f"{self.name}{action.capitalize()}Form"
            model_form_template = None
            if action == "create":
                model_form_template = Template(
                    file=templates.MODEL_CREATE_FORM_TEMPLATE_PATH
                )
            elif action == "update":
                model_form_template = Template(
                    file=templates.MODEL_UPDATE_FORM_TEMPLATE_PATH
                )
            model_form_template.model = self
            model_form_file_path = os.path.join(
                self.model_forms_path, f"{form_class_name}.py"
            )
            # write model form file
            with open(model_form_file_path, "w") as text_file:
                text_file.write(str(model_form_template))
                text_file.close()
            # add import to model forms __init__.py file
            add_import_to_init_file(
                self.model_forms_init_path,
                f"from .{form_class_name} import {form_class_name}\n"
            )
            # add import to app forms __init__.py file
            add_import_to_init_file(
                self.app_forms_init_path,
                f"from .{self.name_lower} import {form_class_name}\n"
            )

    def generate_templates(self):
        Path(self.model_templates_path).mkdir(parents=True, exist_ok=True)
        for action in self.actions:
            t = Template(
                file=templates.getAppTemplatePath(
                    directory="templates",
                    filename=f"template_{action}.tmpl"
                )
            )
            t.settings = settings
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
                file=templates.getAppTemplatePath(
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
            add_import_to_init_file(
                self.model_views_init_file_path,
                f"from .{self.name}{cap_view_name}View import {self.name}{cap_view_name}View\n"
            )
            # add import to __init__.py inside app views path
            add_import_to_init_file(
                self.app_views_init_file_path,
                f"from .{self.name_lower} import {self.name}{cap_view_name}View\n"
            )

        # Generate tests
        Path(self.model_tests_path).mkdir(parents=True, exist_ok=True)
        model_views_test_template = Template(
            file=templates.getAppTemplatePath(
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
        add_import_to_init_file(
            self.model_tests_init_file_path,
            f"from .{self.name}ViewsTest import {self.name}ViewsTest\n"
        )
        # add import to app tests __init__.py
        add_import_to_init_file(
            self.app_tests_init_file_path,
            f"from .{self.name_lower} import {self.name}ViewsTest\n"
        )
        
        # append views to model urls_paths
        for view_name in self.actions:
            cap_view_name = view_name.capitalize()
            # append view path to self.urls_paths list
            # update and delete view
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
                # delete and list view comes here
                self.urls_paths.append((
                    f"{self.name}/{view_name}",
                    f"{self.name}{cap_view_name}View",
                    f"{self.name_lower}-{view_name}"
                ))

    def generate_cbv_urls_routing(self):
        # create app path if not exists
        Path(self.app_path).mkdir(parents=True, exist_ok=True)
        existing_url_patterns = []
        # If url file exists
        if os.path.exists(self.app_urls_file_path):
            # Parse code with RedBaron
            urls_node = RedBaron(file_reader(self.app_urls_file_path))
            existing_url_patterns_nodes = urls_node.find(
                "name", value="urlpatterns").parent.value
            paths = [node.dumps() for node in existing_url_patterns_nodes]
            for url_path in self.urls_paths:
                paths.append(
                    f'path("{url_path[0]}", {url_path[1]}.as_view(), name="{url_path[2]}")')

            string_paths = ",\n\t".join(paths)
            string_paths = f"{string_paths}\n"
            existing_url_patterns_nodes.value = string_paths
            file_writer(self.app_urls_file_path, urls_node.dumps())
            if self.urls_paths:
                append_target_to_from_import(
                    self.app_urls_file_path,
                    f"{self.app_name}.views",
                    targets=[url[1] for url in self.urls_paths]
                )

            # print(existing_url_patterns_nodes.dumps())

        else:
            # if urls.py file not exists
            app_urls_template = Template(
                file=templates.getAppTemplatePath(
                    filename="urls.tmpl"
                )
            )
            app_urls_template.settings = settings
            app_urls_template.urls_paths = self.urls_paths
            app_urls_template.app_name = self.app_name

            file_writer(self.app_urls_file_path, str(app_urls_template))

    def generate_model_python_file(self):
        django_model_template = Template(file=templates.MODEL_TEMPLATE_PATH)
        django_model_template.model = self
        django_model_template.settings = settings
        Path(self.app_models_path).mkdir(parents=True, exist_ok=True)
        # write model file
        with open(self.model_file_path, "w") as text_file:
            text_file.write(str(django_model_template))
            text_file.close()
        # add import to __init__.py
        add_import_to_init_file(
            self.app_models_init_path,
            f"from .{self.name} import {self.name}\n"
        )

    def generate_rest_api(self):
        self.generate_rest_api_serializer()
        self.generate_rest_api_viewset()

        # urls_node = RedBaron(
        #     # Read app urls.py file
        #     # Parse code with RedBaron
        #     file_reader(self.app_urls_file_path)
        # )
        # url_patterns_nodes = urls_node.find(
        #     "name", value="urlpatterns").parent.value
        # existing_urls = [
        #     # get already existed url_patterns
        #     url_pattern_node.dumps() for url_pattern_node in url_patterns_nodes
        # ]
        # existing_urls.append("path('', include(router.urls))")
        # url_patterns_nodes.value = ",\n\t".join(existing_urls) + "\n"
        # file_writer(self.app_urls_file_path.dumps())
        add_import_to_init_file(
            self.app_rest_api_init_file_path,
            ""
        )

    def generate_rest_api_viewset(self):
        Path(
            self.app_rest_api_views_path
        ).mkdir(parents=True, exist_ok=True)
        add_import_to_init_file(
            self.app_rest_api_views_init_file_path,
            f"from .{self.name}ViewSet import {self.name}ViewSet\n"
        )
        django_model_viewset_template = self.get_template_object(
            template_path=templates.REST_API_MODEL_VIEWSET_TEMPLATE_PATH
        )
        file_writer(
            file_path=self.app_rest_api_views_model_viewset_path,
            content=(str(django_model_viewset_template))
        )
        if not os.path.exists(self.app_rest_api_router_path):
            # if app router file not exists
            # generate and write router file
            router_template = self.get_template_object(
                templates.REST_API_ROUTER_TEMPLATE_PATH
            )
            file_writer(self.app_rest_api_router_path, str(router_template))
        else:
            # if exists
            # append modelviewset import import statement
            append_target_to_from_import(
                file_path=self.app_rest_api_router_path,
                import_name=f"{self.app_name}.rest_api.views",
                target=f"{self.name}ViewSet"
            )
            # append the router definition to router file
            file_writer(
                self.app_rest_api_router_path,
                f"router.register(\n\tr'{self.name_lower.lower()}',\n\t{self.name}ViewSet,\n\tbasename='api-{self.name_lower}'\n)\n",
                override=False
            )

    def generate_rest_api_serializer(self):
        # create app/rest_api/serializers path
        Path(
            self.app_rest_api_serializers_path
        ).mkdir(parents=True, exist_ok=True)
        # add to or create init file
        # app/rest_api/serializers/__init__.py
        add_import_to_init_file(
            self.app_rest_api_serializers_init_file_path,
            f"from .{self.name}Serializer import {self.name}Serializer\n"
        )

        django_model_serializer_template = self.get_template_object(
            template_path=templates.REST_API_MODEL_SERIALIZER_TEMPLATE_PATH
        )
        file_writer(
            file_path=self.app_rest_api_serializers_model_serializer_path,
            content=(str(django_model_serializer_template))
        )

    def get_template_object(self, template_path=str):
        template_obj = Template(file=template_path)
        template_obj.model = self
        template_obj.settings = settings
        return template_obj

    def setNamesFromElement(self):
        self.app_name = self.element.attributes.get("namespace").value
        self.name = str(
            self.element.attributes.get(
                "name").value)
        self.name_lower = self.name.lower()
        # use the inflect package to get pluralization
        self.name_plural = inflect.engine().plural(self.name)
        self.name_plural_lower = self.name_plural.lower()
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
            settings.UML2DJANGO_OUTPUT_PATH,
            self.app_name,
        )
        logging.getLogger(__name__).debug(f"OUTPUT_PATH: {settings.UML2DJANGO_OUTPUT_PATH}")
        # App urls.py path
        self.app_urls_file_path = os.path.join(
            self.app_path,
            "urls.py",
        )
        # app Models  directory path
        self.app_models_path = os.path.join(
            self.app_path,
            "models"
        )
        # Models __init__.py path
        self.app_models_init_path = os.path.join(
            self.app_models_path,
            "__init__.py"
        )
        # Model file path
        # example: some_django_app/models/SomeModel.py
        self.model_file_path = os.path.join(
            self.app_models_path,
            f"{self.name}.py"
        )
        # app rest_api path
        # example: some_django_app/rest_api/
        self.app_rest_api_path = os.path.join(
            self.app_path,
            "rest_api"
        )
        # app rest_api path
        # example: some_django_app/rest_api/__init__.py
        self.app_rest_api_init_file_path = os.path.join(
            self.app_rest_api_path,
            "__init__.py"
        )
        # app rest_api router path
        # example: some_django_app/rest_api/router.py
        self.app_rest_api_router_path = os.path.join(
            self.app_rest_api_path,
            "router.py"
        )
        # app rest_api serializers path
        # example: some_django_app/rest_api/serializers
        self.app_rest_api_serializers_path = os.path.join(
            self.app_rest_api_path,
            "serializers"
        )
        # app rest_api serializers init file path
        # example: some_django_app/rest_api/serializers/__init__.py
        self.app_rest_api_serializers_init_file_path = os.path.join(
            self.app_rest_api_serializers_path,
            "__init__.py"
        )
        # app rest_api model serializer path
        # example: some_django_app/rest_api/serializers/SomeModelSerializer.py
        self.app_rest_api_serializers_model_serializer_path = os.path.join(
            self.app_rest_api_serializers_path,
            f"{self.name}Serializer.py"
        )
        # app rest_api views path
        # example: some_django_app/rest_api/views
        self.app_rest_api_views_path = os.path.join(
            self.app_rest_api_path,
            "views"
        )
        # app rest_api views init file path
        # example: some_django_app/rest_api/views/__init__.py
        self.app_rest_api_views_init_file_path = os.path.join(
            self.app_rest_api_views_path,
            "__init__.py"
        )
        # app rest_api model viewset path
        # example: some_django_app/rest_api/views/SomeModelViewSet.py
        self.app_rest_api_views_model_viewset_path = os.path.join(
            self.app_rest_api_views_path,
            f"{self.name}ViewSet.py"
        )

        # App Forms path
        # example: some_django_app/forms/
        self.app_forms_path = os.path.join(
            self.app_path,
            "forms",
        )
        # App Forms __init__.py path
        # example: some_django_app/forms/__init__.py
        self.app_forms_init_path = os.path.join(
            self.app_forms_path,
            "__init__.py"
        )
        # Model Forms path
        # example: some_django_app/forms/somemodel/
        self.model_forms_path = os.path.join(
            self.app_forms_path,
            self.name_lower
        )
        # App Forms __init__.py path
        # example: some_django_app/forms/somemodel/__init__.py
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

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
