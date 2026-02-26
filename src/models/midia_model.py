from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Midia:
    status: bool
    name: Optional[str] = None
    midia_format: Optional[MidiaFormat] = None
    error_msg: Optional[str] = None


class MidiaFormat(Enum):
    VIDEO = "mp4"
    MUSIC = "mp3"
