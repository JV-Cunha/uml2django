import unittest
import os

from uml2django.main import main

__author__ = "Joao Victor Soares da Cunha"


class TestCliArgs(unittest.TestCase):
    # def test_entrypoint(self):
    #     exit_status = os.system('uml2django --help')
    #     self.assertEqual(exit_status, 0)
    
    def test_code_generation(self):
        output_path = "tests/uml2django_output"
        os.system(
            f"uml2django --puml tests/test_project.puml -o {output_path}"
        )
        self.assertTrue(os.path.isdir(output_path))


if __name__ == '__main__':
    unittest.main()
