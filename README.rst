.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://api.cirrus-ci.com/github/<USER>/uml2django.svg?branch=main
    :alt: Built Status
    :target: https://cirrus-ci.com/github/<USER>/uml2django
.. image:: https://readthedocs.org/projects/uml2django/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://uml2django.readthedocs.io/en/stable/
.. image:: https://img.shields.io/coveralls/github/<USER>/uml2django/main.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/<USER>/uml2django
.. image:: https://img.shields.io/pypi/v/uml2django.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/uml2django/
.. image:: https://img.shields.io/conda/vn/conda-forge/uml2django.svg
    :alt: Conda-Forge
    :target: https://anaconda.org/conda-forge/uml2django
.. image:: https://pepy.tech/badge/uml2django/month
    :alt: Monthly Downloads
    :target: https://pepy.tech/project/uml2django
.. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
    :alt: Twitter
    :target: https://twitter.com/uml2django


|

==========
uml2django
==========
Generate `Django <https://www.djangoproject.com/>`_ code from `PlantUML class diagrams <https://plantuml.com/class-diagram>`_

**Syntax**
==========

**Apps**
--------

* To represent an Django App, use the PlantUML ``package`` tag.
* The app name must follow `pep8 <https://peps.python.org/pep-0008/#package-and-module-names>`_:  
    + Modules and packages should have short, all-lowercase names. 
      Underscores can be used in the module name if it improves readability,
      although the use of underscores is discouraged.
        
::

    @startuml
        package exampledjangoapp {
            
        }
        package example_django_app {
            
        }
    @enduml


**Models**
----------
Use PlantUML ``class`` tag to represent an Django Model.
The Model name must follow `pep8 <https://peps.python.org/pep-0008/#class-names>`_ :  
where stands that class names should normally use the CapWords convention.
All models defined MUST BE inside an django_app represented by an plant uml ``package``:: 
    
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



**Fields**
----------

**Model Relationships**
-----------------------
* Inheritance
* Many-to-many
* Many-to-one
* One-to-one


**Documentation**
=================
https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/WritingReST/CheatSheet.html
https://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html
