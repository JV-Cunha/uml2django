import logging
from xml.dom import minidom



def get_xmi_id_of_element(element : minidom.Element):
    element_xmi_id = None
    if element.hasAttribute("xmi.id"):
        element_xmi_id = element.attributes.get("xmi.id").value
        logging.getLogger(__name__).debug(f"element xmi.id {element_xmi_id}")
    else:
        element_xmi_id = element.attributes.get("xmi.idref").value
        logging.getLogger(__name__).debug(f"element xmi.idref {element_xmi_id}")
    return element_xmi_id
