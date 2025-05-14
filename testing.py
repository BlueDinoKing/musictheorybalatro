from models import *
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
    pitch1 = Pitch("C", 5)

    pitches2 = [
        Pitch("C", 5), Pitch("C#", 5), Pitch("Db", 5),
        Pitch("D", 5), Pitch("D#", 5), Pitch("Eb", 5),
        Pitch("E", 5), Pitch("Fb", 5), Pitch("E#", 5),
        Pitch("F", 5), Pitch("F#", 5), Pitch("Gb", 5),
        Pitch("G", 5), Pitch("G#", 5), Pitch("Ab", 5),
        Pitch("A", 5), Pitch("A#", 5), Pitch("Bb", 5),
        Pitch("B", 5), Pitch("Cb", 5), Pitch("B#", 5),
    ]

    interval_names = [
        "Perfect Unison", "Augmented Unison",
        "Minor Second", "Major Second",
        "Augmented Second", "Minor Third", "Major Third",
        "Augmented Third", "Perfect Fourth", "Augmented Fourth",
        "Diminished Fifth", "Perfect Fifth", "Augmented Fifth",
        "Minor Sixth", "Major Sixth", "Augmented Sixth",
        "Diminished Seventh", "Minor Seventh", "Major Seventh"
    ]

    intervals = [
        Interval(pitch1, pitch2) for pitch2 in pitches2
    ]

    for interval, expected_name in zip(intervals, interval_names):
        print(f"Interval: {interval.name}")
        print(f"Notes: {interval.high}, {interval.low}")
        assert interval.name == expected_name



if __name__ == "__main__":
    main()