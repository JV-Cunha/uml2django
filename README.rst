==========
uml2django
==========
uml2django is a tool for generate `Django <https://www.djangoproject.com/>`_ code from `PlantUML class diagrams <https://plantuml.com/class-diagram>`_.
It able to generate: 

* Models
* Forms 
* Class Based Views
* Templates
* Tests

**Quick start**
===============

**Installation**
----------------

* Install via pip::
   
   pip install uml2django

* Download from github::

    git clone https://github.com/J-hanks/uml2django

**Running**
-----------

* From command line::

    uml2django --puml my_plant_uml_class_diagram.puml

* Import as script::

    from uml2django.settings import settings
    from uml2django import objects
    from uml2django import load_data_from

    PLANT_UML_FILE = "school_management_project.puml"
    load_data_from(plantuml_file_path=PLANT_UML_FILE)
    for django_model in objects.DJANGO_MODELS:
        django_model.generate_model_python_file()
        if not django_model.is_abstract:
            django_model.generate_rest_api()
            django_model.generate_model_forms()
            django_model.generate_class_based_views()
            django_model.generate_cbv_urls_routing()
            django_model.generate_templates()

**Syntax**
==========

**Apps**
--------

* To represent an Django App, use the PlantUML ``package`` tag.
* The app name must follow `pep8 <https://peps.python.org/pep-0008/#package-and-module-names>`__:
  *Modules and packages should have short, all-lowercase names.*
  *Underscores can be used if it improves readability,*
  *although the use of underscores is discouraged.*::

    @startuml
        package exampledjangoapp {
            
        }
        package example_django_app {
            
        }
    @enduml


**Models**
----------

* Use PlantUML ``class`` tag to represent an Django Model.
* The Model name must follow `pep8 <https://peps.python.org/pep-0008/#class-names>`__ :  
  *where stands that class names should normally use the CapWords convention.*
* All classes defined MUST BE inside an package, like models inside Django apps.::
    
    @startuml
        package exampledjangoapp {
            class MyFirstModel {

            }
        }
        package example_django_app {
            class MySecondModel {

            }
        }
    @enduml

**Models Inheritance**
----------------------
    
* `Meta inheritance <https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes>`__ ::

    @startuml
        package exampledjangoapp {
            abstract class BaseModel {
                {field} name : CharField(max_length=30)
            }
            class ExtendedModel {
                {field} name : CharField(max_length=30)
            }
            BaseModel <-- ExtendedModel : inherit
        }
    @enduml

* `Multi-table inheritance <https://peps.python.org/pep-0008/#package-and-module-names>`__
* `Proxy inheritance <https://peps.python.org/pep-0008/#package-and-module-names>`__

**Models Relashionships**
-------------------------
* `Many-to-one <https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/#many-to-one-relationships>`__
* `Many-to-many <https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/#many-to-many-relationships>`__
* `One-to-one <https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/#one-to-one-relationships>`__


**Model Fields**
----------------

* Use PlantUML ``{field}`` tag to represent an Django model field.
* If the field type is not informed, uml2django define it as CharField.::

    @startuml
        package exampledjangoapp {
            class MyFirstModel {
                {field} char_field : CharField(max_length=30)
                {field} other_char_field
            }
        }
        package example_django_app {
            class MySecondModel {
                {field} integer_field : IntegerField()
            }
        }
    @enduml
