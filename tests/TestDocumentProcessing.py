import unittest
import os

from uml2django.processDocument import generateXmiFromPuml

__author__ = "Joao Victor Soares da Cunha"


class TestDocumentProcessing(unittest.TestCase):
    # def test_entrypoint(self):
    #     exit_status = os.system('uml2django --help')
    #     self.assertEqual(exit_status, 0)

    def test_generate_xmi_from_puml(self):
        # Should not contain xmi file
        self.assertFalse(os.path.isfile("tests/test_project.xmi"))
        generateXmiFromPuml("tests/test_project.puml")
        self.assertTrue(os.path.isfile("tests/test_project.xmi"))
        os.remove("tests/test_project.xmi")
        self.assertFalse(os.path.isfile("tests/test_project.xmi"))

    def test_generate_xmi_from_puml_file_not_found_exception(self):
        self.assertRaises(
            FileNotFoundError,
            generateXmiFromPuml, "tests/file_not_found.puml"
        )
