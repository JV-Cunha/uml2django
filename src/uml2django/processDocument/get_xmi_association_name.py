from xml.dom import minidom


def get_xmi_association_name(association_element: minidom.Element):
    association_name = association_element.attributes.get(
        "name"
    ).value if association_element.hasAttribute(
        "name"
    ) else None
    if not association_name:
        raise AttributeError("Association must have a name attribute")
    return association_name
