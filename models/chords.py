from models import Pitch, Key, apply_interval
from abc import ABC, abstractmethod

class Chord(ABC):
    """Abstract base class for all chords."""

    def __init__(self, root: Pitch, quality: str, key: Key = None):
        self.root = root
        self.quality = quality
        self.key = key or Key(str(root), "major")
        self.notes = self.generate_notes()

    @abstractmethod
    def generate_notes(self):
        """Generate the chord tones. implemented by subclasses."""
        pass

    def add_note(self, note: Pitch):
        """Add a note to the chord."""
        if note not in self.notes:
            self.notes.append(note)

    def add_notes(self, notes: list):
        """Add multiple notes to the chord."""
        for note in notes:
            self.add_note(note)

    def remove_note(self, note: Pitch):
        """Remove a note from the chord."""
        if note in self.notes:
            self.notes.remove(note)
    def remove_notes(self, notes: list):
        """Remove multiple notes from the chord."""
        for note in notes:
            self.remove_note(note)

    def transpose(self, interval: str):
        """Transpose the chord by a given interval."""
        transposed_root = apply_interval(self.root, self.key, interval)
        self.root = transposed_root
        self.key = Key(str(transposed_root), self.key.mode)
        self.notes = self.generate_notes()

    def __repr__(self):
        return f"{self.root}{self.quality}: {'-'.join(str(n) for n in self.notes)}"


class Triad(Chord):
    """Triad chord: 3-note chords (root, 3rd, 5th)."""

    QUALITY_INTERVALS = {
        "major":      ["M3", "P5"],
        "minor":      ["m3", "P5"],
        "diminished": ["m3", "d5"],
        "augmented":  ["M3", "A5"],
        "suspended2": ["M2", "P5"],
        "suspended4": ["P4", "P5"]
    }

    def generate_notes(self):
        if self.quality not in self.QUALITY_INTERVALS:
            raise ValueError(f"Unsupported triad quality: {self.quality}")
        return [self.root] + [apply_interval(self.root, self.key, intv) for intv in self.QUALITY_INTERVALS[self.quality]]


class SeventhChord(Chord):
    """4-note seventh chords (root, 3rd, 5th, 7th)."""

    QUALITY_INTERVALS = {
        "major7":      ["M3", "P5", "M7"],
        "dominant7":   ["M3", "P5", "m7"],
        "minor7":      ["m3", "P5", "m7"],
        "diminished7": ["m3", "d5", "d7"],
        "half-diminished7": ["m3", "d5", "m7"],
        "minor-major7": ["m3", "P5", "M7"],
        "augmented7":   ["M3", "A5", "m7"]
    }

    def generate_notes(self):
        if self.quality not in self.QUALITY_INTERVALS:
            raise ValueError(f"Unsupported 7th chord quality: {self.quality}")
        return [self.root] + [apply_interval(self.root, self.key, intv) for intv in self.QUALITY_INTERVALS[self.quality]]


class NinthChord(Chord):
    """5-note ninth chords (root, 3rd, 5th, 7th, 9th)."""

    QUALITY_INTERVALS = {
        "major9":    ["M3", "P5", "M7", "M9"],
        "dominant9": ["M3", "P5", "m7", "M9"],
        "minor9":    ["m3", "P5", "m7", "M9"],
        "add9":      ["M3", "P5", "M9"],
        "diminished9": ["m3", "d5", "d7", "m9"],
        "half-diminished9": ["m3", "d5", "m7", "M9"],
        "minor-major9": ["m3", "P5", "M7", "M9"],
        "augmented9": ["M3", "A5", "m7", "M9"]
    }

    def generate_notes(self):
        if self.quality not in self.QUALITY_INTERVALS:
            raise ValueError(f"Unsupported 9th chord quality: {self.quality}")
        return [self.root] + [apply_interval(self.root, self.key, intv) for intv in self.QUALITY_INTERVALS[self.quality]]


