class Pitch:
    letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    wheel = {
        'C': 0, 'B#': 0, 'Dbb': 0,
        'C#': 1, 'Db': 1, 'B##': 1,
        'D': 2, 'Ebb': 2, 'C##': 2,
        'D#': 3, 'Eb': 3, 'Fbb': 3,
        'E': 4, 'Fb': 4,  'D##': 4,
        'E#': 5, 'F': 5,  'Gbb': 5,
        'F#': 6, 'Gb': 6, 'E##': 6,
        'G': 7, 'F##': 7, 'Abb': 7,
        'G#': 8, 'Ab': 8,
        'A': 9, 'G##': 9,   'Bbb': 9,
        'A#': 10, 'Bb': 10, 'Cbb': 10,
        'B': 11, 'Cb': 11 , 'A##': 11,
    }

    def __init__(self, name: str, octave: int = None):
        if name not in self.wheel:
            raise ValueError(f"Invalid pitch name: {name}")
        self.name = name
        self.octave = octave
        self.pc = self.wheel[name]  # pitch class 0-11
        self.letter = name[0]
        self.midi = self._calculate_midi() if octave is not None else None

    def _calculate_midi(self) -> int:
        """Calculate MIDI note number (C4=60, C#4=61, etc.)."""
        return 12 * (self.octave + 1) + self.pc

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


