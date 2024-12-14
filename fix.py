"""
Copy audio files and fix if necessary

- Fix WAV headers, add PCM_16 subtype
"""

import os
from os import path
import shutil

import soundfile

from lib import (
    list_files_and_folders
)

def main():
    """
    Main
    """

    original_audio_dir = "audio"
    fixed_audio_dir = "audio-fixed"

    audio_dirs, audio_files = list_files_and_folders(original_audio_dir)

    for audio_dir in audio_dirs:
        os.makedirs(path.join(fixed_audio_dir, audio_dir), exist_ok=True)

    count = 0
    count_digits = len(str(len(audio_files)))
    for audio_file in audio_files:
        original_path = path.join(original_audio_dir, audio_file)
        fixed_path = path.join(fixed_audio_dir, audio_file)
        count += 1

        file_extension = path.splitext(original_path)[1]
        if file_extension == ".wav":
            print(f"{str(count).zfill(count_digits)} FIX {audio_file}")
            data, samplerate = soundfile.read(original_path)
            soundfile.write(fixed_path, data, samplerate, subtype='PCM_16')
        else:
            print(f"{str(count).zfill(count_digits)} COPY {audio_file}")
            shutil.copy(original_path, fixed_path)

if __name__ == "__main__":
    main()