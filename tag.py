"""
Tag audio files
"""

import re

from lib import (
    load_audio_json,
    store_audio_json,
)

def main():
    """
    Main
    """

    audio = load_audio_json()
    source_types = audio["source_types"]
    source_games = audio["source_games"]
    filters = init_filters()

    # reset all tags, convert to sets
    for audio_file in audio["files"].values():
        audio_file["tags"] = set()

    for source_type in source_types:
        for source_game in source_games:
            # pylint: disable=cell-var-from-loop
            target_files = list(filter(lambda x: x["source_type"] == source_type and x["source_game"] == source_game, audio["files"].values()))

            if source_type in filters:
                for filter_obj in filters["sounds"]:
                    filter_obj.apply(target_files)

    # convert tags back to lists
    for audio_file in audio["files"].values():
        audio_file["tags"] = list(audio_file["tags"])

    store_audio_json(audio)

class NameFilter():
    """
    Tag filter based on file names
    """

    def __init__(self, pattern: str, tags: list[str]):
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.tags = set(tags)

    def apply(self, files: list[dict]):
        """
        Apply filter to files
        """

        hits = 0
        for file in files:
            if self.regex.match(file["file_name"]):
                hits += 1
                file["tags"] = file["tags"] | self.tags

        print(f"Applying filter {self.pattern} to {len(files)} files with {hits} hits")

def init_filters():
    """
    Initialize sounds filters
    """

    filters = {
        "sounds": [

            # Gut
            NameFilter(r"^gu", ["Gut", "Einheit"]),

            # Gut Helden
            NameFilter(r"^gugalad_", ["Held", "Galadriel"]),
            NameFilter(r"^gufrodo_", ["Held", "Frodo"]),
            NameFilter(r"^gutombo_", ["Held", "Tom Bombadil"]),

            # Menschen
            NameFilter(r"^gume", ["Mensch"]),
            NameFilter(r"^gumebui_", ["Baumeister"]),
            NameFilter(r"^gurohir_", ["Rohirim"]),

            # Menschen Helden
            NameFilter(r"^gueomer_", ["Held", "Eomer"]),
            NameFilter(r"^gueowyn_", ["Held", "Eowyn"]),
            NameFilter(r"^gufarra_", ["Held", "Faramir"]),
            NameFilter(r"^gutheod_", ["Held", "Theoden"]),
            NameFilter(r"^guborom_", ["Held", "Boromir"]),
            NameFilter(r"^guarago_", ["Held", "Aragorn"]),
            NameFilter(r"^guganda_", ["Held", "Gandalf"]),

            # Elben
            NameFilter(r"^guel", ["Elb"]),
            NameFilter(r"^guelbui_", ["Baumeister"]),

            # Eleben Helden
            NameFilter(r"^guarwen_", ["Held", "Arwen"]),
            NameFilter(r"^guhaldi_", ["Held", "Haldir"]),
            NameFilter(r"^guglorf_", ["Held", "Glorfindel"]),
            NameFilter(r"^gutreeb_", ["Held", "Baumbart"]),
            NameFilter(r"^guelron_", ["Held", "Elrond"]),
            NameFilter(r"^guthran_", ["Held", "Thranduil"]),
            NameFilter(r"^gulegol_", ["Held", "Legolas"]),

            # Zwerge
            NameFilter(r"^gudw", ["Zwerg"]),
            NameFilter(r"^gudwbui_", ["Baumeister"]),

            # Zwerge Helden
            # prince brand, captain of dale
            NameFilter(r"^gugimli_", ["Held", "Gimli"]),
            NameFilter(r"^gugloin_", ["Held", "Gloin"]),
            # dain ironfoot

            # Böse
            NameFilter(r"^eu", ["Böse", "Einheit"]),

            # Mordor Helfen
            NameFilter(r"^eumouth", ["Mund Saurons"]),

            # Böse Helden
            NameFilter(r"^eusarum_", ["Held", "Saruman"]),
            NameFilter(r"^eugoking_", ["Held", "Gorkil"]),
            NameFilter(r"^eulurtz_", ["Held", "Lurtz"]),
            NameFilter(r"^euwormto_", ["Held", "Schlangenzunge"]),

            NameFilter(r"^euwargr_", ["Wargreiter"]), # isengart?

            # Mordor
            NameFilter(r"^eucorsar", ["Korsaren"]),

            # Voicelines
            NameFilter(r"\w+_voiatt[a-z]", ["Einheit angreifen"]),
            NameFilter(r"\w+_voiatb[a-z]", ["Gebäude angreifen"]),
            NameFilter(r"\w+_voiatc[a-z]", ["? angreifen"]),
            NameFilter(r"\w+_voiam[m|2][a-z]", ["Umgebung"]),
            NameFilter(r"\w+_voidie[a-z]", ["Sterben"]),
            NameFilter(r"\w+_voidiv[a-z]", ["Weggehen"]),
            NameFilter(r"\w+_voidis[a-z]", ["Rückzug?"]),
            NameFilter(r"\w+_voigar[a-z]", ["Turm"]),
            NameFilter(r"\w+_voihu[m|2][a-z]", ["Summen"]),
            NameFilter(r"\w+_voihel[a-z]", ["Hilfe"]),
            NameFilter(r"\w+_voimov[a-z]", ["Bewegen"]),
            NameFilter(r"\w+_voimoc[a-z]", ["Zu Festung"]),
            NameFilter(r"\w+_voimos[a-z]", ["Zu Schiff"]),
            NameFilter(r"\w+_voiret[a-z]", ["Rückzug"]),
            NameFilter(r"\w+_voires[a-z]", ["Wiederbelebt"]),
            NameFilter(r"\w+_voisel[a-z]", ["Auswählen"]),
            NameFilter(r"\w+_voisin[a-z]", ["Singen"]),
            NameFilter(r"\w+_voispe[a-z]", ["Sprechen"]),
            NameFilter(r"\w+_voiseb[a-z]", ["Kampfansage?"]),

        ]
    }

    return filters

if __name__ == "__main__":
    main()
