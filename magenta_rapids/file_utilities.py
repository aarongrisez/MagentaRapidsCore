"""Helper functions for file and directory operations
"""

import os


def check_is_empty_dir(directory: str):
    """Utility function for checking if a directory is empty"""
    for files, directories, _ in os.walk(directory):
        if len(files) > 0 or len(directories) > 0:
            return False
    return True
