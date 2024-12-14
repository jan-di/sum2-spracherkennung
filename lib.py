"""
Shared utility methods
"""

import os
from os import path

def list_files_and_folders(initial_root: str) -> tuple[list, list]:
    """
    List all files and folders in a directory, searching recursively.
    """
    all_dirs = []
    all_files = []

    for root, dirs, files in os.walk(initial_root):
        # Only add leaf folders
        if len(dirs) == 0:
            all_dirs.append(path.relpath(root, initial_root))
        # Add all files
        for name in files:
            all_files.append(path.relpath(path.join(root, name), initial_root))

    return all_dirs, all_files