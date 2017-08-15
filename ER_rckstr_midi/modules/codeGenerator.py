from enum import Enum

NOTE_NAMES = ["C", "Cis", "D", "Dis", "E", "F", "Fis", "G", "Gis", "A", "B", "H"]


class Algorithm(Enum):
    """enum to contain all the possible generator algorithms"""
    DEFAULT = 1
    COUNTER = 2


class CodeGenerator:
    """class to generate numbers and colors from midi data"""

    def __init__(self, algorithm=Algorithm.DEFAULT):
        """constructor
        :param algorithm: select the algorithm from enum with which to generate the number
        """
        self.algorithm = algorithm
        self.calculate_color = True
        self.counter = 0

    def calc_number(self, midi_data=list()):
        """calculates a number from the midi data using the set algorithm
        :param midi_data: midi data to generate number from
        :return: number generated from midi data
        """
        number = 0
        if self.algorithm == Algorithm.DEFAULT:
            for index in range(len(midi_data)):
                if midi_data[index] > 0:
                    number += 2 ** (index % 16)
            number %= 100000
        elif self.algorithm == Algorithm.COUNTER:
            number = self.counter
            self.counter += 1
        else:
            number = 0
        return number

    def calc_color(self, midi_data=list()):
        """calculates the text color from the midi data
        :param midi_data: midi data to render color from
        :return: color calculated from midi data
        """
        if self.calculate_color is False:
            return (255, 255, 255)
        color = 0
        key_counter = 0
        for index in range(len(midi_data)):
            if midi_data[index] > 0:
                key_counter += 1
                color += midi_data[index] * 2
        if key_counter == 0:
            return (0, 0, 0)
        color = color // key_counter
        color = min(color, 255)
        return (color, color, color)

    def calc_note_name(self, midi_data=list(), chord=list()):
        """calculates the name of the note from the midi data
        :param midi_data: midi data to generate note name from
        :param chord: list of notes to verify against
        :return: note name generated from midi data
        """
        name = ""
        key_counter = 0
        key = 0
        for index in range(len(midi_data)):
            if midi_data[index] > 0:
                key = index
                key_counter += 1
        if key_counter == 0:
            name = ""
        elif key_counter > 1:
            if self.verify_chord(midi_data, chord):
                name = "CORRECT"
            else:
                name = "INVALID"
        else:
            key = key % 12
            name = NOTE_NAMES[key]
        return name

    def verify_chord(self, midi_data=list(), chord=list()):
        """verifies the active notes against a list of given notes
        :param midi_data: midi data to verify
        :param chord: list of notes to verify against
        :return: active notes match given chord
        """
        result = True
        for index in range(len(midi_data)):
            if midi_data[index]:
                if index not in chord:
                    result = False
                    break
        for key in chord:
            if not midi_data[key]:
                result = False
                break
        return result
