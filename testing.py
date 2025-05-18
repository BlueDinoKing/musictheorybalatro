from models import *
import pytest
from pytest import main


def test_key():
    """Case 1"""

    # Create a Key object
    key = Key("C", "major")

    # Check the tonic and mode
    assert key.tonic == "C"
    assert key.mode == "major"

    # Check the generated scale
    expected_scale = [
        Pitch("C"), Pitch("D"), Pitch("E"), Pitch("F"),
        Pitch("G"), Pitch("A"), Pitch("B"), Pitch("C")
    ]
    assert key.scale == expected_scale

    # Test invalid mode
    try:
        Key("C", "invalid_mode")
    except ValueError as e:
        assert str(e) == "Unsupported mode: invalid_mode"

    key = Key("Db", "minor")

    assert key.tonic == "C#"
    assert key.mode == "minor"

    expected_scale = [
        Pitch("C#"), Pitch("D#"), Pitch("E"), Pitch("F#"),
        Pitch("G#"), Pitch("A"), Pitch("B"), Pitch("C#")
    ]
    assert key.scale == expected_scale

    try:
        Key("Db", "invalid_mode")
    except ValueError as e:
        assert str(e) == "Unsupported mode: invalid_mode"

def test_pitch():
    """Case 2"""

    # Create a Pitch object
    pitch = Pitch("C", 4)

    # Check the name and octave
    assert pitch.name == "C"
    assert pitch.octave == 4

    # Check the pitch class and letter
    assert pitch.pc == 0
    assert pitch.letter == "C"

    # Test invalid pitch name
    try:
        Pitch("Invalid")
    except ValueError as e:
        assert str(e) == "Invalid pitch name: Invalid"


def test_intervals():
    base = Pitch("C", 5)

    # Pitches spanning C5 up to C7 (two full octaves)
    pitch_names = [
        # Unisons and seconds
        "C", "C#", "Db", "D", "D#", "Eb",
        # Thirds
        "Ebb", "E", "Fb", "E#",
        # Fourths
        "F", "F#", "Gb",
        # Fifths
        "G", "G#", "Ab",
        # Sixths
        "A", "A#",
        # Sevenths
        "Bb", "Bbb", "B", "Cb", "B#6",
        # Octaves
        "C6", "C#6", "D6", "E6", "F6", "G6", "A6", "B6", "C7"
    ]

    expected_names = [
        "U", "AU", "m2", "M2", "A2", "m3",
        "d3", "M3", "d4", "A3",
        "P4", "A4", "d5",
        "P5", "A5", "m6",
        "M6", "A6",
        "m7", "d7", "M7", "d8", "A7",
        "P8", "A8", "M9", "M10", "P11",
        "P12", "M13", "M14", "P15"
    ]

    # Convert pitch names to Pitch objects
    def make_pitch(name):
        if name[-1].isdigit():
            if name[-2] in "#b":
                return Pitch(name[:-1], int(name[-1]))
            else:
                return Pitch(name[:-1], int(name[-1]))
        return Pitch(name, 5)

    pitches = [make_pitch(name) for name in pitch_names]
    intervals = [Interval(base, p) for p in pitches]

    for interval, expected in zip(intervals, expected_names):
        # print(f"{interval.low} to {interval.high} → {interval.name}: {expected == interval.name}."
        #       f" {interval.semitones}, {interval.letter_steps}")
        assert interval.name == expected

def test_add_interval():
    base = Pitch("C", 5)

    # Test adding intervals
    new_pitch = apply_interval(base, Key("C"), "d5")
    assert new_pitch == Pitch("Gb", 5)

    new_pitch = apply_interval(base, Key("C"), "P5")
    assert new_pitch == Pitch("G", 5)

    new_pitch = apply_interval(base, Key("C"), "A5")
    assert new_pitch == Pitch("G#", 5)

    new_pitch = apply_interval(base, Key("C"), "P8")
    assert new_pitch == Pitch("C", 6)

    new_pitch = apply_interval(base, Key("C"), "A4")
    assert new_pitch == Pitch("F#", 5)


    # Test invalid interval
    try:
        apply_interval(base, Key("A"), "Invalid")
    except ValueError as e:
        assert str(e) == "Unsupported interval: Invalid"

@pytest.mark.parametrize("root, quality, exp, mode", [
    ("C", "major",      ["C", "E", "G"],        "major"),
    ("D", "minor",      ["D", "F", "A"],        "minor"),
    ("E", "diminished", ["E", "G", "Bb"],       "diminished"),
    ("F", "augmented",  ["F", "A", "C#"],       "augmented"),
    ("G", "suspended2", ["G", "A", "D"],        "major"),
    ("A", "suspended4", ["A", "D", "E"],        "major"),
    ("Ab", "major",     ["Ab", "C", "Eb"],      "major"),
])
def test_valid_triads(root, quality, exp, mode):
    root = Pitch(root)
    key = Key(str(root), mode)
    triad = Triad(root, quality, key)

    expected_notes = [Pitch(p) for p in exp]

    assert triad.root == root
    assert triad.quality == quality
    assert triad.notes == expected_notes


def test_invalid_quality():
    with pytest.raises(ValueError) as exc_info:
        Triad(Pitch("C"), "invalid_quality", Key("C"))
    assert "Unsupported triad quality" in str(exc_info.value)

@pytest.mark.parametrize("root, quality, exp, mode", [
    ("C", "major7",      ["C", "E", "G", "B"],         "major"),
    ("D", "dominant7",   ["D", "F#", "A", "C"],        "major"),
    ("E", "minor7",      ["E", "G", "B", "D"],         "minor"),
    ("F", "diminished7", ["F", "Ab", "Cb", "Ebb"],     "diminished"),
    ("G", "half-diminished7", ["G", "Bb", "Db", "F"],  "minor"),
    ("Ab", "minor-major7", ["Ab", "Cb", "Eb", "G"],    "minor"),
])
def test_valid_sevenths(root, quality, exp, mode):
    root = Pitch(root)
    key = Key(str(root), mode)
    seventh = SeventhChord(root, quality, key)

    expected_notes = [Pitch(p) for p in exp]

    assert seventh.root == root
    assert seventh.quality == quality
    assert seventh.notes == expected_notes
def test_invalid_seventh_quality():
    with pytest.raises(ValueError) as exc_info:
        SeventhChord(Pitch("C"), "invalid_quality", Key("C"))
    assert "Unsupported 7th chord quality" in str(exc_info.value)

@pytest.mark.parametrize("root, quality, exp, mode", [
    ("C", "major9",      ["C", "E", "G", "B", "D"],        "major"),
    ("D", "dominant9",   ["D", "F#", "A", "C", "E"],       "major"),
    ("E", "minor9",      ["E", "G", "B", "D", "F#"],        "minor"),
    ("F", "diminished9", ["F", "Ab", "Cb", "Ebb", "Gb"],     "diminished"),
    ("G", "half-diminished9", ["G", "Bb", "Db", "F", "A"],  "minor"),
])

def test_valid_ninths(root, quality, exp, mode):
    root = Pitch(root)
    key = Key(str(root), mode)
    ninth = NinthChord(root, quality, key)

    expected_notes = [Pitch(p) for p in exp]

    assert ninth.root == root
    assert ninth.quality == quality
    assert ninth.notes == expected_notes


def test_invalid_ninth_quality():
    with pytest.raises(ValueError) as exc_info:
        NinthChord(Pitch("C"), "invalid_quality", Key("C"))
    assert "Unsupported 9th chord quality" in str(exc_info.value)

def test_compliment():
    interval = Interval(Pitch("C"), Pitch("Gb"))
    assert interval.compliment() == Interval(Pitch("C"), Pitch("F#"))


@pytest.mark.parametrize("expected_root, quality, notes, expected_type", [
    # Exact matches
    (Pitch("C"), "major", [Pitch("C"), Pitch("E"), Pitch("G")], Triad),
    (Pitch("C"), "minor", [Pitch("C"), Pitch("Eb"), Pitch("G")], Triad),
    (Pitch("D"), "augmented", [Pitch("D"), Pitch("F#"), Pitch("A#")], Triad),
    (Pitch("F"), "major7", [Pitch("F"), Pitch("A"), Pitch("C"), Pitch("E")], SeventhChord),
    (Pitch("G"), "dominant9", [Pitch("G"), Pitch("B"), Pitch("D"), Pitch("F"), Pitch("A")], NinthChord),

    # Inversions
    (Pitch("C"), "major", [Pitch("E"), Pitch("G"), Pitch("C")], Triad),
    (Pitch("C"), "minor", [Pitch("Eb"), Pitch("G"), Pitch("C")], Triad),
    (Pitch("F"), "major7", [Pitch("A"), Pitch("C"), Pitch("E"), Pitch("F")], SeventhChord),
])
def test_find_chord(expected_root, quality, notes, expected_type):
    # Exact match
    chord = find_chord(notes)
    assert isinstance(chord, expected_type)
    assert chord.root == expected_root
    assert chord.quality == quality

def test_generic_chord_fallback():
    notes = [Pitch("C"), Pitch("D"), Pitch("F#")]  # doesn't match any known chord
    chord = find_chord(notes)
    assert isinstance(chord, GenericChord)









if __name__ == "__main__":
    main()