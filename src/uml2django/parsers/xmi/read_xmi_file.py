from xml.dom import minidom


def read_xmi_file(filename: str) -> minidom.Document:
    """Try to Read XMI File from given filename

    Args:
        filename (str): _description_

    Returns:
        minidom.Document: Returns the document object model
    """
    document_object_model = None
    # Try to read from given filename, exits if file not found
    try:
        document_object_model = minidom.parse(filename)
    except OSError as e:
        print(e)

    return document_object_model
