"""Mutator classes for Magenta Rapids. A mutator is responsible for
mutating a MIDI bytestream, and must implement the `mutate` method. `mutate`
must return a bytestream containing the mutated MIDI messages.
"""

import abc
import io
import os
import typing as t
import mido


# pylint: disable=too-few-public-methods
class AbstractMutator(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def mutate(self, file_object: t.BinaryIO, number_steps: int) -> t.BinaryIO:
        raise NotImplementedError


# pylint: disable=too-few-public-methods
class SimpleMutator(AbstractMutator):
    def __init__(self, *args, **kwargs):
        pass

    def __alter_note(self, message: mido.Message) -> mido.Message:
        if message.type == "note_off":
            note_off_delay = 50
        else:
            note_off_delay = 0
        return message.copy(
            time=int(
                message.time
                + note_off_delay
                + (
                    (60 / message.note**2)
                    * (message.time**1.1 + message.note**1.9)
                )
            )
        )

    def mutate(self, file_object: t.BinaryIO, number_steps: int) -> t.BinaryIO:
        file_object.seek(os.SEEK_SET)
        file = mido.MidiFile(file=file_object)
        file_object.seek(os.SEEK_SET)
        for track in file.tracks:
            for idx, message in enumerate(track):
                if message.type in ("note_on", "note_off"):
                    for _ in range(number_steps):
                        message = self.__alter_note(message)
                    track[idx] = message
        new_file_object = t.cast(t.BinaryIO, io.BytesIO())
        file.save(file=new_file_object)
        new_file_object.seek(os.SEEK_SET)
        return new_file_object
