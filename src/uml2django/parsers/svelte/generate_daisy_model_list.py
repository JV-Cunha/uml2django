import os
from pathlib import Path
from uml2django.objects.DjangoModel import DjangoModel
from uml2django.parsers.files.file_writer import file_writer
from uml2django.settings import settings
from uml2django.templates import SVELTE_DAISY_ROUTES_LIST_PATH


def generate_daisy_model_list(django_model: DjangoModel):
    svelte_daisy_model_list_template = django_model.get_template_object(
        template_path=SVELTE_DAISY_ROUTES_LIST_PATH
    )
    output_path = os.path.join(
        settings.UML2DJANGO_OUTPUT_PATH,
        "svelte_app", "src", "routes",
        f"{django_model.app_name}", f"{django_model.name_lower}"
    )
    Path(output_path).mkdir(parents=True, exist_ok=True)
    svelte_model_list_path = os.path.join(
        output_path,
        "list.svelte"
    )
    file_writer(
        file_path=svelte_model_list_path,
        content=(str(svelte_daisy_model_list_template))
    )

