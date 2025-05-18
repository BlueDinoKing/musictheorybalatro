import json
from models import Pitch, Key, Triad, SeventhChord, NinthChord, GenericChord
from itertools import permutations

# Load precomputed chord data
with open("models/chords_by_type.json") as f:
    CHORD_DB = json.load(f)

CHORD_CLASS_MAP = {
    "triad": Triad,
    "seventh": SeventhChord,
    "ninth": NinthChord
}

def normalize_semitones(root_pc, note_pcs):
    return sorted((pc - root_pc) % 12 for pc in note_pcs)

def find_chord(notes, allow_fuzzy=False):
    fuzzy_matches = []
    if not notes:
        return None

    note_pcs = [note.pc for note in notes]

    # Try all permutations as possible inversions
    for perm in permutations(notes):
        root = perm[0]
        relative_semitones = normalize_semitones(root.pc, note_pcs)

        for chord_type, roots in CHORD_DB.items():
            for root_name, qualities in roots.items():
                for quality, data in qualities.items():
                    target = sorted(data["semitones"])

                    if relative_semitones == target:
                        root_pitch = root
                        key = Key(str(root), "major")
                        chord_class = CHORD_CLASS_MAP.get(chord_type, GenericChord)
                        return chord_class(root_pitch, quality, key)

                    if allow_fuzzy:
                        match_count = len(set(relative_semitones).intersection(set(target)))
                        required = len(target) - 1  # allow one note to be missing
                        if match_count >= required:
                            fuzzy_matches.append((root, quality, chord_type))

    if fuzzy_matches:
        # fallback to first fuzzy match
        root, quality, chord_type = fuzzy_matches[0]
        key = Key(str(root), "major")
        chord_class = CHORD_CLASS_MAP.get(chord_type, GenericChord)
        return chord_class(root, quality, key)

    return GenericChord(notes)
