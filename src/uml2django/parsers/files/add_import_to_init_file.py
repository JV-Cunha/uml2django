from os.path import exists as file_exists

def add_import_to_init_file(
        init_file_path: str, import_statement: str
) -> None:
    """Checks if init file already has the import statement
    and add it if not.

    Args:
        init_file_path (str): The __init__.py file path
        import_statement (str): The import statement to add after check if exists
    """

    already_has_import_statement = False
    init_file_exists = False
    # If init file exists
    if file_exists(init_file_path):
        init_file_exists = True
        # open with read permissions
        with open(init_file_path, "r") as init_file:
            # Check if import statement already exists in init_file
            if import_statement in init_file.read():
                already_has_import_statement = True
            init_file.close()

    if not already_has_import_statement:
        # open the file with append permissions
        mode = "a" if init_file_exists else "w"
        with open(init_file_path, mode) as init_file:
            init_file.write(import_statement)
            init_file.close()
