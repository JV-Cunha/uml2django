
import logging
import sys
from xml.dom import minidom
from uml2django.settings import settings


class DjangoModelField():
    name = None
    field_type = None
    field_options = None
    visibility = None
    unique = False
    uml2django_field_options = []

    def __init__(self, element: minidom.Element = None):
        if not element:
            logging.getLogger(__name__).debug("An element must be given")
            sys.exit(1)
        self.element = element
        visibility_attr = element.attributes.get("visibility")
        if visibility_attr:
            if visibility_attr.value == "protected":
                self.unique = True
                logging.getLogger(__name__).debug(f"{self.name} UNIQUE ")
        self.set_name_from_element()
        self.fillNameAndFieldType()


    def __str__(self) -> str:
        return f"{self.name} - {self.field_type}"

    def set_name_from_element(self):
        name_and_field = self.element.attributes.get("name").value
        name_and_field = name_and_field.split(":")

        name = name_and_field[0]
        name = name.split(" ")
        name = "_".join(list(filter(None, name)))
        self.name = name

    def fillNameAndFieldType(self) -> None:
        # If no field type was informed
        # Set as CharField
        name_and_field = self.element.attributes.get("name").value
        name_and_field = name_and_field.split(":")
        if len(name_and_field) == 1:
            self.field_type = "CharField"
            self.field_options = [
                f"max_length={settings.UML2DJANGO_CHAR_FIELD_MAX_LENGTH}"]
        else:
            field = name_and_field[1]
            field = field.split(" ")
            field = "".join(list(filter(None, field)))
            self.field_type = field[:field.find("(")]
            # remove () from field string
            self.field_options = field[field.find(
                "(")+1:field.find(")")].split(",")
            # remove blank spaces
            self.field_options = list(filter(None, self.field_options))

        has_verbose_name = False
        has_help_text = False
        char_field_has_max_length = False
        foreign_key_has_on_delete = False
        foreign_key_has_related_name = False
        foreign_key_has_related_query_name = False
        # loop through field options and values
        
        for field_option in self.field_options:
            # if field options is 'verbose_name'
            has_verbose_name = True if field_option.startswith(
                "verbose_name") else False
            # if field options is 'help_text'
            has_help_text = True if field_option.startswith(
                "help_text") else False
            
            # if field type is char field
            if self.field_type == "CharField":
                # check if have a 'max_length' option
                char_field_has_max_length = True if field_option.startswith(
                    "max_length") else False
        

            # if field type is ForeignKey
            if self.field_type == "ForeignKey":
                if field_option.startswith("uml2django_"):
                    self.uml2django_field_options.append(field_option)
                    self.field_options.remove(field_option)
                foreign_key_has_on_delete = True if field_option.startswith(
                    "on_delete") else False
                foreign_key_has_related_name = True if field_option.startswith(
                    "related_name") else False
                foreign_key_has_related_query_name = True if field_option.startswith(
                    "related_query_name") else False
        
        if self.unique:
            self.field_options.append("unique=True")
            
        if not has_verbose_name:
            verbose_name = " ".join(self.name.split("_"))
            self.field_options.append(f"verbose_name=_('{verbose_name}')")
        if not has_help_text and settings.UML2DJANGO_GENERATE_FIELDS_HELP_TEXT:
            self.field_options.append(
                f"help_text=_('{verbose_name} help text')")

        if not char_field_has_max_length and self.field_type == "CharField":
            self.field_options.append(
                f"max_length={settings.UML2DJANGO_CHAR_FIELD_MAX_LENGTH}")
            # s = field
            # field_options = s[s.find("(")+1:s.find(")")]

        if self.field_type == "ForeignKey" and not foreign_key_has_on_delete:
            self.field_options.append(
                f"on_delete={settings.UML2DJANGO_FOREIGNKEY_ON_DELETE}"
            )
        
        
        # if self.field_type == "ForeignKey" and not foreign_key_has_related_name:
        #     # self.field_options.append(
        #         # f"related_name={}"
        #     # )
