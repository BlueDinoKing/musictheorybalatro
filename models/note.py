class Pitch:
    letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    wheel = {
        'C': 0, 'B#': 0,
        'C#': 1, 'Db': 1,
        'D': 2,
        'D#': 3, 'Eb': 3,
        'E': 4, 'Fb': 4,
        'E#': 5, 'F': 5,
        'F#': 6, 'Gb': 6,
        'G': 7,
        'G#': 8, 'Ab': 8,
        'A': 9,
        'A#': 10, 'Bb': 10,
        'B': 11, 'Cb': 11
    }

    def __init__(self, name: str, octave: int = None):
        if name not in self.wheel:
            raise ValueError(f"Invalid pitch name: {name}")
        self.name = name
        self.octave = octave
        self.pc = self.wheel[name]  # pitch class 0-11
        self.letter = name[0]

    def __repr__(self):
        return f"{self.name}{'' if self.octave is None else self.octave}"

    def semitone_distance(self, other) -> int:
        return abs(self.pc - other.pc + 12 * ((self.octave or 0) - (other.octave or 0)))

    def letter_distance(self, other) -> int:
        return (Pitch.letters.index(other.letter) - Pitch.letters.index(self.letter)) % 7

    def __eq__(self, other):
        if isinstance(other, Pitch):
            if self.octave is None or other.octave is None:
                return self.pc == other.pc
            return self.pc == other.pc and self.octave == other.octave
        return False


class Interval:
    qualities = {
        (0, 0): "Perfect Unison", (1, 0): "Augmented Unison",
        (1, 1): "Minor Second", (2, 1): "Major Second", (3, 1): "Augmented Second",
        (3, 2): "Minor Third", (4, 2): "Major Third", (5, 2): "Augmented Third",
        (5, 3): "Perfect Fourth", (6, 3): "Augmented Fourth",
        (6, 4): "Diminished Fifth", (7, 4): "Perfect Fifth", (8, 4): "Augmented Fifth",
        (8, 5): "Minor Sixth", (9, 5): "Major Sixth", (10, 5): "Augmented Sixth",
        (9, 6): "Diminished Seventh", (10, 6): "Minor Seventh", (11, 6): "Major Seventh",
        (12, 7): "Perfect Octave"
    }

    def __init__(self, low: Pitch, high: Pitch):
        # The issue was here: we need to ensure high is actually higher than low
        # before calculating the interval
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
        return self.qualities.get((self.semitones % 12, self.letter_steps % 7), f"{self.semitones} semitones")

    def __repr__(self):
        return self.name