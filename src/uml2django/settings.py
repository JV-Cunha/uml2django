from xml.dom.expatbuilder import DOCUMENT_NODE


class settings:
    DOCUMENT_OBJECT_MODEL = None
    DJANGO_MODELS = None

    UML2DJANGO_GENERATE_DJANGO_PROJECT = True
    UML2DJANGO_GENERATE_DJANGO_INSTALLED_APPS_REQUIREMENTS = [
        "rest_framework",
        "crispy_forms"
    ]
    UML2DJANGO_PROJECT_NAME = None
    UML2DJANGO_APPS_NAMES = []
    UML2DJANGO_OUTPUT_PATH = "uml2django_output"
    UML2DJANGO_OVERRIDE = True
    
    UML2DJANGO_GENERATE_REST_APIS = True
    UML2DJANGO_REST_APIS_BROWSABLE = True

    UML2DJANGO_GENERATE_FIELDS_HELP_TEXT = True
    UML2DJANGO_CHAR_FIELD_SHORTCUT = "CF"
    UML2DJANGO_CHAR_FIELD_MAX_LENGTH = 255

    UML2DJANGO_DECIMAL_FIELD_SHORTCUT = "DF"
    UML2DJANGO_DECIMAL_FIELD_DECIMAL_PLACES = 4
    UML2DJANGO_DECIMAL_FIELD_MAX_DIGITS = 11

    UML2DJANGO_USE_DJANGO_CRISPY_FORMS = True
    UML2DJANGO_USE_BASE_TEMPLATE = True
    UML2DJANGO_BASE_TEMPLATE = "base.html"
    UML2DJANGO_BASE_TEMPLATE_CONTENT_BLOCK_NAME = "base_content"
    UML2DJANGO_USE_I18N = True
