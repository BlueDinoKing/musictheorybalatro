from models import Pitch

class Key:
    # Semitone patterns for each mode
    mode_patterns = {
        "major":      [2, 2, 1, 2, 2, 2, 1],  # Ionian
        "dorian":     [2, 1, 2, 2, 2, 1, 2],
        "phrygian":   [1, 2, 2, 2, 1, 2, 2],
        "lydian":     [2, 2, 2, 1, 2, 2, 1],
        "mixolydian": [2, 2, 1, 2, 2, 1, 2],
        "minor":      [2, 1, 2, 2, 1, 2, 2],  # Aeolian
        "aeolian":    [2, 1, 2, 2, 1, 2, 2],
        "locrian":    [1, 2, 2, 1, 2, 2, 2],
        "diminished": [1, 2, 1, 2, 1, 2, 1],
        "augmented":  [2, 1, 2, 1, 2, 1, 2],
        "whole_tone": [2, 2, 2, 2, 2, 2],     # Whole Tone
        "chromatic":  [1] * 12,               # Chromatic
        "blues":      [3, 2, 1, 1, 3, 2],     # Blues
        "pentatonic": [2, 2, 3, 2, 3],        # Pentatonic
        "natural_minor": [2, 1, 2, 2, 1, 2, 2], # Natural Minor
        "harmonic_minor": [2, 1, 2, 2, 1, 3, 1], # Harmonic Minor
        "melodic_minor": [2, 1, 2, 2, 2, 2, 1], # Melodic Minor
    }

    # Standard enharmonic spelling map for keys (especially minor)
    tonic_normalization = {
        "Cb": "B",  "B#": "C",
        "Fb": "E",  "E#": "F",
        "Gb": "F#", "F##": "G",
        "Ab": "G#", "G##": "A",
        "Bb": "A#", "A##": "B",
        "Db": "C#", "C##": "D",
        "Eb": "D#", "D##": "E"
    }

    def __init__(self, tonic: str, mode: str = "major"):
        self.original_tonic = tonic
        self.mode = mode.lower()
        if self.mode not in self.mode_patterns:
            raise ValueError(f"Unsupported mode: {mode}")
        self.tonic = self.normalize_tonic(tonic)
        self.scale = self.generate_scale()

    def normalize_tonic(self, tonic: str):
        """Use enharmonic spelling preferred for common keys (e.g., Gb → F#)."""
        if tonic in self.tonic_normalization:
            return self.tonic_normalization[tonic]
        return tonic

    def generate_scale(self):
        steps = self.mode_patterns[self.mode]
        scale = [Pitch(self.tonic)]
        current_pc = scale[0].pc
        current_letter_index = Pitch.letters.index(self.tonic[0])

        for step in steps:
            current_pc = (current_pc + step) % 12
            current_letter_index = (current_letter_index + 1) % 7
            expected_letter = Pitch.letters[current_letter_index]
            note = self.find_spelling(current_pc, expected_letter)
            scale.append(Pitch(note))
        return scale

    def find_spelling(self, target_pc, letter):
        for name, pc in Pitch.wheel.items():
            if pc == target_pc and name[0] == letter:
                return name
        raise ValueError(f"Can't find spelling for pitch class {target_pc} and letter {letter}")

    def __repr__(self):
        scale_str = " ".join(str(p) for p in self.scale)
        return f"{self.original_tonic} {self.mode.capitalize()}"

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.tonic == other.tonic and self.mode == other.mode
        return False