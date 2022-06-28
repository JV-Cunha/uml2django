import unittest
import os

from uml2django.parsers.files import generate_xmi_from_puml, get_django_models_from_xmi_document, read_xmi_file
from uml2django.objects import DjangoModel

__author__ = "Joao Victor Soares da Cunha"


class TestDocumentProcessing(unittest.TestCase):
    # def test_entrypoint(self):
    #     exit_status = os.system('uml2django --help')
    #     self.assertEqual(exit_status, 0)
    MODELS_COUNT = 2
    PLANT_UML_FILE = "tests/test_project.puml"
    XMI_FILE = "tests/test_project.xmi"

    def test_generate_model_l(self):
        # Should not contain xmi file
        self.assertFalse(os.path.isfile(self.XMI_FILE))
        generate_xmi_from_puml(self.PLANT_UML_FILE)
        self.assertTrue(os.path.isfile(self.XMI_FILE))
        os.remove(self.XMI_FILE)
        self.assertFalse(os.path.isfile(self.XMI_FILE))

    def test_generate_xmi_from_puml_file_not_found_exception(self):
        self.assertRaises(
            FileNotFoundError,
            generate_xmi_from_puml, "tests/file_not_found.puml"
        )

    def test_read_xmi_file(self):
        generate_xmi_from_puml(self.PLANT_UML_FILE)
        document_object_model = read_xmi_file(self.XMI_FILE)
        django_models = get_django_models_from_xmi_document(
            document_object_model
        )
        self.assertEqual(len(django_models), self.MODELS_COUNT)
        os.remove(self.XMI_FILE)
        