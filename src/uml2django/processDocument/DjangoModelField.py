import sys
from xml.dom import minidom
from uml2django.config import (
    CHAR_FIELD_MAX_LENGTH,
)
from uml2django.logger import _logger


class DjangoModelField():
    name = None
    field_type = None
    field_options = None
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

        # If no field type was informed
        if len(name_and_field) == 1:
            self.field_type = "CharField"
            self.field_options = [f"max_length={CHAR_FIELD_MAX_LENGTH}"]
        else:
            field = name_and_field[1]
            field = field.split(" ")
            field = "".join(list(filter(None, field)))
            self.field_type = field[:field.find("(")]
            self.field_options = field[field.find("(")+1:field.find(")")].split(",")
            self.field_options = list(filter(None, self.field_options))
        
        has_verbose_name = False
        for field_option in self.field_options:
            has_verbose_name = True if field_option.startswith("verbose_name") else False
        if not has_verbose_name:
            verbose_name = " ".join(self.name.split("_"))
            self.field_options.append(f"verbose_name=_('{verbose_name}')")
            
            # s = field
            # field_options = s[s.find("(")+1:s.find(")")]
