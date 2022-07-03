from uml2django.parsers.svelte.generate_daisy_model_list import generate_daisy_model_list
from uml2django.parsers.svelte.start_svelte_app import start_svelte_app
from uml2django.settings import settings
from uml2django import objects
from uml2django import load_data_from

PLANT_UML_FILE = "school_management_project.puml"
load_data_from(plantuml_file_path=PLANT_UML_FILE)
start_svelte_app()
for django_model in objects.DJANGO_MODELS:
    generate_daisy_model_list(django_model)
    # generate_carbon_model_form(django_model)
    # django_model.generate_model_python_file()
    # if not django_model.is_abstract:
        # django_model.generate_rest_api()
        # django_model.generate_model_forms()
        # django_model.generate_class_based_views()
        # django_model.generate_cbv_urls_routing()
        # django_model.generate_templates()

