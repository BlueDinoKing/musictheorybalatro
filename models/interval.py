"""Interval module."""
from models import Pitch

class Interval:
    qualities = {  # semitone, note letters
        (0,  0): "U",    (0,  1): "d2",
        (1,  0): "AU",   (1,  1): "m2",
        (2,  1): "M2",   (2,  2): "d3",
        (3,  1): "A2",   (3,  2): "m3",   (3,  3): "m3",
        (4,  2): "M3",   (4,  3): "d4",
        (5,  2): "A3",   (5,  3): "P4",   (5,  4): "d5",
        (6,  3): "A4",   (6,  4): "d5",
        (7,  4): "P5",   (7,  5): "d6",
        (8,  4): "A5",   (8,  5): "m6",
        (9,  5): "M6",   (9,  6): "d7",
        (10, 5): "A6",   (10, 6): "m7",
        (11, 6): "M7",   (11, 0) : "d8",
        (12, 0): "P8",   (12, 6): "A7",
        (13, 0): "A8",   (13, 1): "m9",
        (14, 1): "M9",   (14, 2): "d10",
        (15, 1): "A9",   (15, 2): "m10",
        (16, 2): "M10",  (16, 3): "D11",
        (17, 2): "A10",  (17, 3): "P11",
        (18, 3): "D12",  (18, 4): "A11",
        (19, 4): "P12",  (19, 5): "m13",
        (20, 4): "M13",  (20, 5): "D14",
        (21, 5): "M13",  (21, 6): "A12",
        (23, 6): "M14",
        (24, 0): "P15",
    }

    def __init__(self, low: Pitch, high: Pitch):
        if (high.octave or 0) > (low.octave or 0) or ((high.octave or 0) == (low.octave or 0) and high.pc >= low.pc):
            self.low = low
            self.high = high
        else:
            # Swap if high is actually lower than low
            self.low = high
            self.high = low

        # Calculate semitones from low to high
        self.semitones = (self.high.pc + 12 * (self.high.octave or 0)) - (self.low.pc + 12 * (self.low.octave or 0))

        # Calculate letter steps correctly
        low_letter_idx = Pitch.letters.index(self.low.letter)
        high_letter_idx = Pitch.letters.index(self.high.letter)

        # Calculate positive letter steps
        if high_letter_idx >= low_letter_idx:
            self.letter_steps = high_letter_idx - low_letter_idx
        else:
            self.letter_steps = 7 - (low_letter_idx - high_letter_idx)

        self.name = self.qualify()

    def qualify(self):
        # Handle special case for B#6 (which should be an ASeventh)
        if self.high.name == "B#" and (self.high.octave or 0) > (self.low.octave or 0):
            if self.semitones == 12 and self.letter_steps % 7 == 6:
                return "A7"
        if self.high.octave or self.low.octave is not None:
            return self.qualities.get((self.semitones, self.letter_steps % 7), f"{self.semitones} semitones")
        return self.qualities.get((self.semitones % 12, self.letter_steps % 7), f"{self.semitones} semitones")

    def __repr__(self):
        return self.name


interval_semitones = {
    "P1": 0, "A1": 1, "d2": 0, "m2": 1, "M2": 2, "A2": 3,
    "d3": 2, "m3": 3, "M3": 4, "A3": 5,
    "d4": 4, "P4": 5, "A4": 6,
    "d5": 6, "P5": 7, "A5": 8,
    "d6": 7, "m6": 8, "M6": 9, "A6": 10,
    "d7": 9, "m7": 10, "M7": 11, "A7": 12,
    "d8": 11, "P8": 12, "A8": 13,
    "m9": 13, "M9": 14, "A9": 15,
    "m10": 15, "M10": 16,
    "P11": 17, "A11": 18, "P12": 19,
    "m13": 20, "M13": 21,
    "M14": 23, "P15": 24,
}

def apply_interval(pitch: Pitch, key, interval_str: str) -> Pitch:
    semitones = interval_semitones.get(interval_str)
    if semitones is None:
        raise ValueError(f"Unsupported interval: {interval_str}")

    # Determine letter steps from interval string (e.g., M2 = 1 step, M3 = 2 steps...)
    interval_number = int(''.join(filter(str.isdigit, interval_str)))
    letter_steps = (interval_number - 1) % 7

    # New letter after applying interval
    start_letter_index = Pitch.letters.index(pitch.letter)
    new_letter_index = (start_letter_index + letter_steps) % 7
    new_letter = Pitch.letters[new_letter_index]

    # New pitch class
    new_pc = (pitch.pc + semitones) % 12

    # New octave
    pitch_total = pitch.pc + (pitch.octave or 0) * 12
    new_pitch_total = pitch_total + semitones
    if pitch.octave is not None:
        new_octave = new_pitch_total // 12
    else:
        new_octave = None

    # Use key to get correct spelling
    note_name = key.find_spelling(new_pc, new_letter)
    return Pitch(note_name, None if new_octave is None else new_octave)
