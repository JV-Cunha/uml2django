from xml.dom import minidom
from uml2django.parsers.xmi.XmiArgoUmlTagsNames import XMI_ARGO_CLASS_ABSTRACT_ATTRIBUTE


def is_xmi_element_abstract(element: minidom.Element) -> bool:
    """Check if given element is abstract or not

    Args:
        element (minidom.Element): The XMI element to check.

    Returns:
        bool: True if it is abstract, False if not
    """    
    if element.hasAttribute(XMI_ARGO_CLASS_ABSTRACT_ATTRIBUTE):
        is_abs = element.attributes.get(XMI_ARGO_CLASS_ABSTRACT_ATTRIBUTE).value
        return True if is_abs == "true" else False
    else:
        return False
