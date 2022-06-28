import logging
from xml.dom import minidom
# from uml2django import _logger

from uml2django.parsers.xmi.XmiArgoUmlTagsNames import XMI_ARGO_CLASS_TAG_NAME
from uml2django.objects.DjangoModel import DjangoModel


def get_django_models_from_xmi_document(
    document: minidom.Document
) -> list:
        """
        Classes whitout name are used to represent association,
        they have xmi_id attribute setted instead

        :param document: the minidom.Document object instance
        :type document: minidom.Document
        :return: The List with DjangoModels Objects
        :rtype: List[DjangoModel]
        """
        django_models = []
        class_elements = document.documentElement.getElementsByTagName(
            XMI_ARGO_CLASS_TAG_NAME
        )

        for class_element in class_elements:
            # Get the only xmi classes that have its name attribute setted
            if class_element.attributes.get("name") is not None:
                # initialize DjangoModel
                django_model = DjangoModel(class_element)
                django_models.append(django_model)
        logging.getLogger(__name__).debug(f"FOUND {len(django_models)} MODELS")
        return django_models
