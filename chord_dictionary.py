import json
from collections import defaultdict
from models import Triad, SeventhChord, NinthChord, Pitch, Key

def make_chords_hierarchical():
    """Generate a nested dictionary of chords organized by type -> root -> quality."""
    chord_classes = {
        "triad": {
            "major": Triad,
            "minor": Triad,
            "diminished": Triad,
            "augmented": Triad,
            "suspended2": Triad,
            "suspended4": Triad
        },
        "seventh": {
            "major7": SeventhChord,
            "dominant7": SeventhChord,
            "minor7": SeventhChord,
            "diminished7": SeventhChord,
            "half-diminished7": SeventhChord,
            "minor-major7": SeventhChord,
            "augmented7": SeventhChord
        },
        "ninth": {
            "major9": NinthChord,
            "dominant9": NinthChord,
            "minor9": NinthChord,
            "add9": NinthChord,
            "diminished9": NinthChord,
            "half-diminished9": NinthChord,
            "minor-major9": NinthChord,
            "augmented9": NinthChord
        }
    }

    roots = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
    output = defaultdict(lambda: defaultdict(dict))

    for chord_type, qualities in chord_classes.items():
        for quality, chord_cls in qualities.items():
            for root_name in roots:
                root = Pitch(root_name)
                key = Key(str(root), "major")
                try:
                    chord = chord_cls(root, quality, key)
                    output[chord_type][root_name][quality] = {
                        "notes": [str(n) for n in chord.notes],
                        "semitones": sorted((n.pc - root.pc) % 12 for n in chord.notes)
                    }
                except Exception:
                    print(f"Error creating {chord_type} chord: {root_name} {quality}")
                    continue

    return output

if __name__ == "__main__":
    data = make_chords_hierarchical()
    with open("models/chords_by_type.json", "w") as f:
        json.dump(data, f, indent=2)
    print("chords_by_type.json generated successfully.")
