"""
Copy audio files and fix if necessary

- Fix WAV headers, add PCM_16 subtype
"""

import os
from os import path
import shutil
import hashlib

import soundfile

from lib import (
    list_files_and_folders,
    load_audio_json,
    store_audio_json,
)

def main():
    """
    Main
    """

    original_audio_dir = "audio"
    fixed_audio_dir = "audio-fixed"
    audio = load_audio_json()

    audio_dirs, audio_files = list_files_and_folders(original_audio_dir)

    for audio_dir in audio_dirs:
        os.makedirs(path.join(fixed_audio_dir, audio_dir), exist_ok=True)

    count = 0
    count_digits = len(str(len(audio_files)))
    source_types = set()
    source_games = set()

    for audio_file in audio_files:
        original_path = path.join(original_audio_dir, audio_file)
        fixed_path = path.join(fixed_audio_dir, audio_file)
        count += 1

        file_name, file_extension = path.splitext(path.basename(original_path))
        source_type = path.basename(path.dirname(original_path))
        source_game = path.basename(path.dirname(path.dirname(original_path)))


        if file_extension in [".wav", ".mp3"]:
            duration = None
            # Fix WAV headers
            if file_extension == ".wav":
                print(f"{str(count).zfill(count_digits)} FIX  {audio_file}")
                data, samplerate = soundfile.read(original_path)
                soundfile.write(fixed_path, data, samplerate, subtype='PCM_16')

                # get duration of wav file
                duration = len(data) / samplerate

            else:
                if file_extension == ".mp3":
                    # get duration of mp3 file
                    duration = soundfile.info(original_path).duration

                print(f"{str(count).zfill(count_digits)} COPY {audio_file}")
                shutil.copy(original_path, fixed_path)

            # Store information in audio JSON
            if audio_file not in audio["files"]:
                audio_file_dict = {}
            else:
                audio_file_dict = audio["files"][audio_file]

            audio_file_dict["file_name"] = file_name
            audio_file_dict["file_ext"] = file_extension
            audio_file_dict["source_type"] = source_type
            audio_file_dict["source_game"] = source_game
            audio_file_dict["duration"] = round(duration, 1)
            audio_file_dict["uid"] = hashlib.md5(f"{source_game}-{source_type}-{file_name}".encode('utf-8')).hexdigest()

            source_types.add(source_type)
            source_games.add(source_game)

        else:
            print(f"{str(count).zfill(count_digits)} SKIP {audio_file}")

    audio["source_types"] = list(source_types)
    audio["source_games"] = list(source_games)

    store_audio_json(audio)

if __name__ == "__main__":
    main()
