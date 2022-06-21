

def file_writer(file_path: str, content: str, override=True):
    if override:
        with open(file_path, "w") as file:
            file.write(str(content))
            file.close()
