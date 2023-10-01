import os

def check_is_empty_dir(dir: str):
    """Utility function for checking if a directory is empty
    """
    for files, directories, _ in os.walk(dir):
        if len(files) > 0 or len(directories) > 0:
            return False
    