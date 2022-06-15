from uml2django import settings
from uml2django import _logger
from uml2django.XmiArgoUmlTagsNames import (
    XMI_ARGO_ASSOCIATION_TAG_NAME, XMI_ARGO_CLASS_TAG_NAME
)
from uml2django.processDocument import find_django_model_by_xmi_id, get_xmi_association_name, get_xmi_id_of_element


def load_associations():
    # Get all association elements in document
    association_elements = settings.DOCUMENT_OBJECT_MODEL.documentElement.getElementsByTagName(
        XMI_ARGO_ASSOCIATION_TAG_NAME
    )
    _logger.debug(f"Found {len(association_elements)} associations elements")

    # loop through each association element
    for association_element in association_elements:
        # get association name attribute
        association_name = get_xmi_association_name(association_element)
        
        # if is an inheritance
        if association_name == "inherit":
            _logger.debug("Inheritance association")
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
                model = find_django_model_by_xmi_id(
                    association_class_element_xmi_id
                )
                associated_models.append(
                    model
                )
            
            _logger.debug(f"associated models: {[str(model) for model in associated_models]}")
            abstract_model = None
            not_abstract_model = None
            base_model = associated_models[0]
            extended_model = associated_models[1]
            extended_model.add_base_father(base_model)