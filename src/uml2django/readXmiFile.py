from xml.dom import minidom


def readXmiFile(filename: str) -> minidom.Document:
    """Try to Read XMI File from given filename

    :return: Returns the document object model
    :rtype: minidom.Document
    """
    document_object_model = None
    # Try to read from given filename, exits if file not found
    try:
        document_object_model = minidom.parse(filename)
    except OSError as e:
        print(e)
        
        
        # sys.exit(1)

    # print(document_object_model.documentElement.getElementsByTagName('UML:Namespace.ownedElement'))
    # print(document_object_model.documentElement.childNodes)

    return document_object_model
