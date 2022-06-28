from os.path import exists


def file_reader(file_path: str) -> str:
    content = ""
    with open(file_path, "r") as file:
        # Parse code with RedBaron
        content = file.read()
        file.close()
    return content
