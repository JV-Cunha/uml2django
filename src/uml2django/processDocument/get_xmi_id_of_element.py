from xml.dom import minidom

from uml2django import _logger


def get_xmi_id_of_element(element : minidom.Element):
    element_xmi_id = None
    if element.hasAttribute("xmi.id"):
        element_xmi_id = element.attributes.get("xmi.id").value
        _logger.debug(f"element xmi.id {element_xmi_id}")
    else:
        element_xmi_id = element.attributes.get("xmi.idref").value
        _logger.debug(f"element xmi.idref {element_xmi_id}")
    return element_xmi_id
