import os
from pathlib import Path
import shutil
from django.core import management as django_management

from redbaron import RedBaron

from uml2django import settings, _logger


def start_django_project():
    # start project command
    django_management.call_command(
        'startproject',
        (
            f"{settings.UML2DJANGO_PROJECT_NAME}",
            f"{settings.UML2DJANGO_OUTPUT_PATH}"
        )
    )
    _logger.debug("Created Django Project")
    # start apps
    for app_name in settings.UML2DJANGO_APPS_NAMES:
        app_path = os.path.join(
            f"{settings.UML2DJANGO_OUTPUT_PATH}",
            f"{app_name}"
        )
        Path(app_path).mkdir(
            parents=True, exist_ok=True
        )
        django_management.call_command(
            'startapp',
            (
                f"{app_name}",
                app_path
            )
        )
        os.remove(os.path.join(app_path, "models.py"))
        os.remove(os.path.join(app_path, "views.py"))
        os.remove(os.path.join(app_path, "tests.py"))
        # os.remove(os.path.join(app_path, "urls.py"))

    # add apps to settings.py
    django_project_settings_file_path = os.path.join(
        settings.UML2DJANGO_OUTPUT_PATH,
        settings.UML2DJANGO_PROJECT_NAME,
        "settings.py"
    )
    settings_node = None
    with open(django_project_settings_file_path, "r") as source:
        _logger.debug("OPEN settings.py")
        # Parse code with RedBaron
        settings_node = RedBaron(source.read())
        source.close()
    installed_apps_node = settings_node.find(
        "name", value="INSTALLED_APPS"
    ).parent.value
    installed_apps_names_list = []
    # Add already existing apps in INSTALLED_APPS
    # to array installed_apps_names_list
    for installed_app in installed_apps_node.value:
        installed_apps_names_list.append(str(installed_app.value))
    # Extend installed apps with apps generated by uml2django
    installed_apps_names_list.extend(
        # embrace each app name with ''
        [f"'{app_name}'" for app_name in settings.UML2DJANGO_APPS_NAMES]
    )
    # joins the apps names in a string
    # and set ins the installed app in settins.py
    installed_apps_node.value = ",\n\t".join(installed_apps_names_list)

    # write settings.py
    with open(django_project_settings_file_path, "w") as source:
        source.write(settings_node.dumps())
        source.close()
        
    # add apps urls to project urls.py
    django_project_urls_file_path = os.path.join(
        settings.UML2DJANGO_OUTPUT_PATH,
        settings.UML2DJANGO_PROJECT_NAME,
        "urls.py"
    )
    # Read project urls.py file
    urls_node = None
    with open(django_project_urls_file_path, "r") as source:
        # Parse code with RedBaron
        urls_node = RedBaron(source.read())
        source.close()
    
    # get url_patterns_nodes
    existing_url_patterns_nodes = urls_node.find("name", value="urlpatterns").parent.value
    # append already existed url_patterns
    existing_urls = []
    for existing_url_pattern_node in existing_url_patterns_nodes:
        existing_urls.append(existing_url_pattern_node.dumps())
        
    # append the include directive for each app_name 
    for app_name in settings.UML2DJANGO_APPS_NAMES:
        existing_urls.append(f"path('/', include('{app_name}.urls'))")
        
    # Set the urls_patterns nodes value
    # by joining the array
    existing_url_patterns_nodes.value = ",\n".join(existing_urls)
    
    # write the the modified code to
    # django project urls file 
    with open(django_project_urls_file_path, "w") as source:
        source.write(urls_node.dumps())
        source.close()
        