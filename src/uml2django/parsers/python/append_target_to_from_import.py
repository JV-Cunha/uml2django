import logging
from redbaron import RedBaron
from uml2django.parsers.files.file_reader import file_reader
from uml2django.parsers.files.file_writer import file_writer


def append_target_to_from_import(
    file_path: str, import_name: str,
    target="", targets=[]
):
    
    if not target and not targets:
        raise AttributeError("Must have an target to append")
    # clean targets to avoid bugs
    targets = [] if not targets else targets
    # append target to targets
    if target:
        targets.append(target)
    
    logging.getLogger(__name__).debug(f"APPENDING {targets} to {import_name}")
    # read file and parse to RedBaron object
    file_node = RedBaron(file_reader(file_path))
    # get all from import nodes
    from_imports_nodes = file_node.find_all("from_import")
    for router_import_node in from_imports_nodes:
        # loop through nodes
        if len(router_import_node.value) == len(import_name.split(".")):
            constructed_import_name = ".".join(
                # joins the array get from import name values
                [
                    # the import name pieces
                    str(value) for value in router_import_node.value
                ]
            )
            if import_name == constructed_import_name:
                # if equals
                # get targets
                import_targets = [
                    target.value for target in router_import_node.targets
                ]
                if import_targets[0] == "(":
                    import_targets = import_targets[1:-1]
                for target in targets:
                    if target not in import_targets:
                        import_targets.append(f"{target}")
                string_targets = ",\n\t".join(import_targets)
                string_targets = f"(\n\t{string_targets}\n)"
                router_import_node.targets = string_targets

    file_writer(file_path, file_node.dumps())