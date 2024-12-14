"""
Shared utility methods
"""

import os
from os import path
import json

AUDIO_JSON = "audio.json"

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

def load_audio_json(audio_file: str = AUDIO_JSON) -> dict:
    """
    Load audio JSON file
    """
    try:
        with open(audio_file, "r", encoding="utf8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "source_types": [],
            "source_games": [],
            "files": {}
        }

def store_audio_json(data: dict, audio_file: str = AUDIO_JSON):
    """
    Store audio JSON file
    """
    with open(audio_file, "w", encoding="utf8") as file:
        json.dump(data, file, indent=4)