import logging
from uml2django.settings import settings
from uml2django.parsers.xmi.XmiArgoUmlTagsNames import (
    XMI_ARGO_ASSOCIATION_TAG_NAME, XMI_ARGO_CLASS_TAG_NAME
)
from uml2django.parsers.settings.find_loaded_django_model_by_xmi_id import find_loaded_django_model_by_xmi_id
from uml2django.parsers.xmi.get_name_of_element import get_name_from_element
from uml2django.parsers.xmi.get_xmi_id_of_element import get_xmi_id_of_element


def load_associations():
    # Get all association elements in document
    association_elements = settings.DOCUMENT_OBJECT_MODEL.documentElement.getElementsByTagName(
        XMI_ARGO_ASSOCIATION_TAG_NAME
    )
    logging.getLogger(__name__).debug(f"Found {len(association_elements)} associations elements")

    # loop through each association element
    for association_element in association_elements:
        # get association name attribute
        association_name = get_name_from_element(association_element)
        
        # if is an inheritance
        if association_name == "inherit":
            logging.getLogger(__name__).debug("Inheritance association")
            # get the classes elements inside the association element
            association_classes_elements = association_element.getElementsByTagName(
                XMI_ARGO_CLASS_TAG_NAME
            )
            # association must have 2 classes elements 
            if len(association_classes_elements) != 2:
                raise AttributeError("Association don't have 2 classes")

            associated_models = list()
            for association_class_element in association_classes_elements:
                association_class_element_xmi_id = get_xmi_id_of_element(
                    association_class_element
                )
                
                model = find_loaded_django_model_by_xmi_id(
                    association_class_element_xmi_id
                )
                associated_models.append(
                    model
                )
            
            logging.getLogger(__name__).debug(f"associated models: {[str(model) for model in associated_models]}")
            base_model = associated_models[0]
            extended_model = associated_models[1]
            extended_model.add_base_father(base_model)