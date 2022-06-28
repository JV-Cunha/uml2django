from redbaron import RedBaron



def file_writer(file_path: str, content: str, override=True):
    mode = "w" if override else "a"
    with open(file_path, mode) as file:
        file.write(str(content))
        file.close()
