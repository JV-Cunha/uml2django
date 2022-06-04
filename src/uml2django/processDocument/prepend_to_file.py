def prepend_to_file(file_path, content):
    """ Add content to begin of the file  """
    file = open(file_path, 'r+', encoding='utf-8')
    lines = file.readlines()
    file.seek(0)
    file.write(content)
    for line in lines:  # write old content after new
        file.write(line)
    file.close
