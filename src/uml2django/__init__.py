import sys


if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError






# for dom_element in root_element.childNodes:
    #     _logger.debug(dom_element.parentNode)
    #     if dom_element.__class__ == minidom.Element:
    #         if dom_element.tagName == XmiArgoUmlTagsName.XMI_ARGO_CLASS_TAG_NAME:
    #             (classes_without_associations.append(dom_element))
    #             
                    

    # print(classes_without_associations)
    # for class_without_association in classes_without_associations:
        # class_name = class_without_association.attributes.get("name").value.lower().capitalize()
        
        # template_file_content = read_file(template_file_path)
        #     template_rendered = string.Template(template_file_content).safe_substitute(
        #         app_name=app_name,
        #         model_name=model_name,
        #         model_name_u_lower=model_name_underscore,
        #         model_name_lower=model_name.lower(),
        #         crud_item=crud_item,
        #         crud_item_capitalize=crud_item.capitalize()
        #     )
    # print(associations)