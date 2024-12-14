"""
Transcribe all audio files
"""
from os import path

import speech_recognition as sr

from lib import (
    load_audio_json,
    store_audio_json,
)

def main():
    """
    Main
    """

    # Load audio information
    audio = load_audio_json()
    r = sr.Recognizer()

    current_count = 0
    total_count = len(audio["files"])
    count_digits = len(str(total_count))
    for audio_file_path, audio_file in audio["files"].items():
        current_count += 1
        progress_percent = (current_count / total_count) * 100
        progress_str = f"{str(current_count).rjust(count_digits)} ({str(round(progress_percent, 1)).rjust(5)}%)"

        # Store audio information every 20 files, to prevent losses due to crashes
        if current_count % 20 == 0:
            store_audio_json(audio)

        # Skip non-wav files, as speech_recognition only supports wav files
        if audio_file["file_ext"] not in [".wav"]:
            print(f"{progress_str} SKIP {audio_file_path} (not transcribable)")
            continue

        # Skip files that have already been transcribed via google
        if "google_transcribed" in audio_file and audio_file["google_transcribed"]:
            print(f"{progress_str} SKIP {audio_file_path} (already transcribed via google)")
            continue

        print(f"{progress_str} START {audio_file_path}..")
        full_audio_path = path.join("audio-fixed", audio_file_path)

        with sr.AudioFile(full_audio_path) as source:
            audio_data = r.record(source)

        transcribed_text = None
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            transcribed_text = r.recognize_google(audio_data, language="de-DE")
            print(f"{progress_str} TEXT {audio_file_path}: {transcribed_text}")
        except sr.UnknownValueError:
            print(f"{progress_str} NULL {audio_file_path}")

        except sr.RequestError as e:
            print(f"{progress_str} ERR {audio_file_path}: {e}")
            break

        audio["files"][audio_file_path]["google_transcribed"] = True
        audio["files"][audio_file_path]["google_transcribed_text"] = transcribed_text

    # Store audio information
    store_audio_json(audio)


if __name__ == "__main__":
    main()
