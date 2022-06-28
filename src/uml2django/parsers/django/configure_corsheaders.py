import os
from os.path import exists as file_exists

from uml2django.settings import settings
from redbaron import RedBaron

from uml2django.parsers.files.file_reader import file_reader
from uml2django.parsers.files.file_writer import file_writer


def configure_corsheaders() -> None:

    django_project_settings_file_path = os.path.join(
        settings.UML2DJANGO_OUTPUT_PATH,
        settings.UML2DJANGO_PROJECT_NAME,
        "settings.py"
    )
    django_project_settings_node = RedBaron(
        # Read project settings.py file
        # Parse code with RedBaron
        file_reader(django_project_settings_file_path)
    )
    django_project_settings_node.find_all("from_import")
    existing_middlewares_nodes = django_project_settings_node.find(
        "name", value="MIDDLEWARE").parent.value
    middlewares = [node.dumps() for node in existing_middlewares_nodes]
    middlewares.insert(2, "'corsheaders.middleware.CorsMiddleware'")
    string_middlewares = ",\n\t".join(middlewares)
    string_middlewares = f"{string_middlewares}\n"
    existing_middlewares_nodes.value = string_middlewares
    file_writer(django_project_settings_file_path,
                django_project_settings_node.dumps())
    file_writer(
        django_project_settings_file_path,
        "\nCORS_ALLOWED_ORIGINS = [\"http://127.0.0.1:3000\"]\n",
        override=False
    )
