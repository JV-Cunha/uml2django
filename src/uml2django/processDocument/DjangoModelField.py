import sys
from xml.dom import minidom
from uml2django.logger import _logger


class DjangoModelField():
    name = None
    field_type = None
    visibility = None
    
    def __init__(self, element: minidom.Element = None):
        if not element:
            _logger.debug("An element must be given")
            sys.exit(1)
        self.element = element
        self.fillNameAndFieldType()
        v = element.attributes.get("visibility")
        if v:
            _logger.debug(f"{self.name} = {self.field_type}")
            
    def __str__(self) -> str:
        return f"{self.name} - {self.field_type}"

    def fillNameAndFieldType(self) -> None:
        """Fill the name and field of DjangoModelAttribute class
        element is expected to have it`s name attribute as one of the follow options

        name
        name : Charfield
        birth_date : DateField
        birth date : DateField
        
        A CharField is used when no field type is given.

        Args:
            element (minidom.Element): The attribute element
        """        
        name_and_field = self.element.attributes.get("name").value
        name_and_field = name_and_field.split(":")

        name = name_and_field[0]
        name = name.split(" ")
        name = "_".join(list(filter(None, name)))
        self.name = name

        if len(name_and_field) == 1:
            self.field_type = "CharField"
        else:
            field = name_and_field[1]
            field = field.split(" ")
            field = "".join(list(filter(None, field)))
            self.field_type = field


