import argparse
import math
from typing import List

STANDARD_A = 440  # Orchestra standard A


class ChromaticScale:
    CHROMATIC_A_INDEX = 3

    def __init__(self, base_a=STANDARD_A):
        self._base_freq = base_a

    def __getitem__(self, index: int):
        return self.to_frequency(index)

    def to_frequency(self, index: int) -> float:
        return self._base_freq * 2 ** ((index + ChromaticScale.CHROMATIC_A_INDEX) / 12)

    def to_index(self, freq: float) -> int:
        half_steps = 12 * math.log2(freq / self._base_freq)
        index = round(half_steps - ChromaticScale.CHROMATIC_A_INDEX)
        return index


STANDARD_CHROMATIC = ChromaticScale()
NOTES_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


class Chord:
    def __init__(self, name: str, notes):
        self.name = name
        self.notes = notes
        self.__dict__.update({note.name: note for note in self.notes})


def note_from_freq(freq: float, chromatic_scale=STANDARD_CHROMATIC):
    name = NOTES_NAMES[chromatic_scale.to_index(freq) % len(NOTES_NAMES)]
    return Note(name, freq)


class Note:
    def __init__(self, name: str, freq: float, chromatic_scale=STANDARD_CHROMATIC):
        self.name = name
        self.freq = freq
        self.chromatic_scale = chromatic_scale

    def from_freq(self, freq: float):
        name = NOTES_NAMES[self.chromatic_scale.to_index(freq) % len(NOTES_NAMES)]
        return Note(name, freq)

    def get_chord_notes(self, offsets: List[int]):
        chromatic_index = self.chromatic_scale.to_index(self.freq)
        chord_notes = [note_from_freq(self.chromatic_scale.to_frequency(chromatic_index + offset)) for offset in
                       offsets]
        return chord_notes

    def major(self) -> Chord:
        return Chord(self.name, self.get_chord_notes([0, 4, 7]))

    def major7(self) -> Chord:
        return Chord(f"{self.name}maj7", self.get_chord_notes([0, 4, 7, 11]))

    def minor(self) -> Chord:
        return Chord(f"{self.name}m", self.get_chord_notes([0, 3, 7]))

    def minor7(self) -> Chord:
        return Chord(f"{self.name}m7", self.get_chord_notes([0, 3, 7, 10]))

    def dominant(self) -> Chord:
        return Chord(f"{self.name}7", self.get_chord_notes([0, 4, 7, 10]))

    def half_diminished(self) -> Chord:
        return Chord(f"{self.name}m7b5", self.get_chord_notes([0, 3, 6, 10]))

    def diminished(self) -> Chord:
        return Chord(f"{self.name}dim7", self.get_chord_notes([0, 3, 6, 9]))

    def octave_up(self):
        self.freq *= 2

    def octave_down(self):
        self.freq /= 2


notes = [note_from_freq(STANDARD_CHROMATIC[i]) for i in range(len(NOTES_NAMES))]

chords = {"init": [("major", {chord.name: chord for chord in [note.major() for note in notes]}),
                   ("major7", {chord.name: chord for chord in [note.major7() for note in notes]}),
                   ("minor", {chord.name: chord for chord in [note.minor() for note in notes]}),
                   ("minor7", {chord.name: chord for chord in [note.minor7() for note in notes]}),
                   ("dominant", {chord.name: chord for chord in [note.dominant() for note in notes]}),
                   ("half_diminished", {chord.name: chord for chord in [note.half_diminished() for note in notes]}),
                   ("diminished", {chord.name: chord for chord in [note.diminished() for note in notes]}),
                   ]}


# create a function to reduce namespace garbage
def setup_chords(chords):
    for chord_family_name, chord_family_dict in chords["init"]:
        chords[chord_family_name] = argparse.Namespace(**chord_family_dict)
        for chord_name in chord_family_dict:
            chords[chord_name] = chord_family_dict[chord_name]
    chords.pop("init")
    return chords


chords = setup_chords(chords)

notes = argparse.Namespace(**{note.name: note for note in notes})

chords = argparse.Namespace(**chords)
