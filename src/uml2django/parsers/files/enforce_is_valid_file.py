import os
import errno


def is_valid_file(file_path: str) -> bool:
    """Checks that filename given as argument is a valid file

    Args:
        parser (argparse.ArgumentParser): The ArgumentParser instance
        arg (str): The filename given as argument

    Returns:
        str: The filename given as argument
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), file_path
        )
    else:
        return True