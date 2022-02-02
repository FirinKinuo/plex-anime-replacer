from enum import Enum
from typing import TypedDict
from pathlib import Path


class AnimeProviders(Enum):
    ANILIBRIA = 'anilibria'


class AnimeFileType(Enum):
    SERIAL = 'serial'
    FUll_LENGTH = 'full-length'
    SPECIAL = 'special'


class AnimeMetaData(TypedDict):
    path: Path
    name: str
    extension: str
    episode: int
    season: str
