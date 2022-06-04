import unittest
import os

from uml2django.main import main

__author__ = "Joao Victor Soares da Cunha"


class TestCliCodeGeneration(unittest.TestCase):
    # def test_entrypoint(self):
    #     exit_status = os.system('uml2django --help')
    #     self.assertEqual(exit_status, 0)

    def test_generated_file_structure(self):
        output_path = "tests/uml2django_output"
        apps = [
            {
                "name": "testapp",
                "models": [
                    {
                        "name": "ExampleTestModel"
                    }
                ]
            },
        ]
        os.system(
            f"uml2django --puml tests/test_project.puml -o {output_path}"
        )
        self.assertTrue(os.path.isdir(output_path))
        # check apps_paths
        for app in apps:
            app_path = os.path.join(output_path, app["name"])
            self.assertTrue(os.path.isdir(app_path))





