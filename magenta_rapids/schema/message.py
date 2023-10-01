from typing import Optional, List, Union
from enum import StrEnum
from pydantic import BaseModel

class MessageType(StrEnum):
    NOTE_ON="Note On"
    NOTE_OFF="Note Off"
    CONTROL_CHANGE="Control Change"
    PROGRAM_CHANGE="Program Change"
    AFTER_TOUCH="After Touch"
    PITCH_BEND_CHANGE="Pitch Bend Change"

class NoteOnMessage:
    