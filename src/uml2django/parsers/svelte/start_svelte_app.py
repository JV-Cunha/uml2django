import os
from pathlib import Path
import shutil
import subprocess
from Cheetah.Template import Template

from uml2django import objects, templates
from uml2django.objects.find_loaded_django_models_by_app_name import find_loaded_django_models_by_app_name
from uml2django.parsers.files.file_writer import file_writer
from uml2django.parsers.xmi.read_xmi_file import read_xmi_file
from uml2django.settings import settings
from uml2django.templates import getSvelteDaisyTemplate


class UI_LIBRARY:
    CARBON = "carbon"
    DAISY = "daisy"


svelte_app_path = os.path.join(
    settings.UML2DJANGO_OUTPUT_PATH,
    "svelte_app"
)


def install_dev_dependency(dependency: str):
    subprocess.run(
        [
            "npm",
            "install",
            "-D",
            dependency
        ],
        cwd=svelte_app_path)


def start_svelte_app(ui_library=UI_LIBRARY.DAISY):

    if os.path.exists(svelte_app_path):
        shutil.rmtree(svelte_app_path)

    Path(svelte_app_path).mkdir(
        parents=True, exist_ok=True
    )
    # subprocess.check_call('npm --help', shell=True)
    subprocess.run(["npm", "create", "svelte"], cwd=svelte_app_path)
    subprocess.run(["npm", "install"], cwd=svelte_app_path)
    install_dev_dependency("uuid")

    if ui_library == UI_LIBRARY.DAISY:
        install_dev_dependency("daisyui")
        install_dev_dependency("@steeze-ui/svelte-icon")
        install_dev_dependency("@steeze-ui/heroicons")

        # copy tailwind config
        tailwind_config_file_name = "tailwind.config.cjs"
        tailwind_config_template_path = getSvelteDaisyTemplate(
            tailwind_config_file_name
        )
        shutil.copyfile(
            tailwind_config_template_path,
            os.path.join(svelte_app_path, tailwind_config_file_name)
        )
        # copy postcss config
        postcss_config_file_name = "postcss.config.cjs"
        postcss_config_template_path = getSvelteDaisyTemplate(
            postcss_config_file_name
        )
        shutil.copyfile(
            postcss_config_template_path,
            os.path.join(svelte_app_path, postcss_config_file_name)
        )
        # crate tailwind.css and append imports
        svelte_app_src_tailwind_css_file_path = os.path.join(
            svelte_app_path, "src",
            "tailwind.css")
        file_writer(
            file_path=svelte_app_src_tailwind_css_file_path,
            content="@tailwind base;\n@tailwind components;\n@tailwind utilities;"
        )

        # override layout with template
        layout_template_path = getSvelteDaisyTemplate(
            "daisy_layout.svelte.tmpl")
        svelte_app_path_layout_path = os.path.join(
            svelte_app_path, "src", "routes", "__layout.svelte"
        )
        os.remove(svelte_app_path_layout_path) if os.path.isfile(
            svelte_app_path_layout_path) else None
        shutil.copyfile(
            layout_template_path,
            svelte_app_path_layout_path,
        )

        # copy lib path
        svelte_app_lib_path = os.path.join(
            svelte_app_path, "src", "lib"
        )
        Path(svelte_app_lib_path).mkdir(
            parents=True, exist_ok=True
        )
        for file in os.listdir(templates.SVELTE_DAISY_LIB):
            file_path = os.path.join(templates.SVELTE_DAISY_LIB, file)
            if not os.path.isdir(os.path.abspath(file_path)):
                if not templates.SVELTE_DAISY_LIB_SIDEBAR.endswith(file):
                    shutil.copyfile(
                        os.path.join(templates.SVELTE_DAISY_LIB, file),
                        os.path.join(svelte_app_lib_path,
                                     file[:-5] if file.endswith("tmpl") else file)
                    )
            else:
                shutil.copytree(
                    file_path, os.path.join(svelte_app_lib_path, file),
                    symlinks=False, ignore=None,
                    ignore_dangling_symlinks=False, dirs_exist_ok=True,
                )

        # fill sidebar
        side_bar_template_obj = Template(
            file=templates.SVELTE_DAISY_LIB_SIDEBAR)
        apps_and_its_models = {}
        for app_name in objects.UML2DJANGO_APPS_NAMES:
            apps_and_its_models[app_name] = find_loaded_django_models_by_app_name(
                app_name)
        side_bar_template_obj.apps_and_its_models = apps_and_its_models
        file_writer(
            file_path=os.path.join(
                svelte_app_lib_path, "Sidebar.svelte"
            ),
            content=str(side_bar_template_obj)
        )

        src = os.path.join(
            templates.SVELTE_DAISY_ROUTES_PATH, 'account'
        )
        dst = os.path.join(
            svelte_app_path, 'src', 'routes', 'account'
        )
        shutil.copytree(
            src, dst, symlinks=False, ignore=None,
            ignore_dangling_symlinks=False, dirs_exist_ok=False
        )
