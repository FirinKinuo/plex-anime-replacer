import re
from pathlib import Path
from logging import getLogger
from typing import Union

from replacer.settings import config

log = getLogger(__name__)

VIDEO_FORMATS = [
    '.3gp', '.asf', '.avi', '.flv', '.m2ts', '.m4v', '.mkv',
    '.mov', '.mp4', '.mts', '.ogg', '.vob', '.wmv', '.webm'
]

SEASON_SPECIALS = ['OVA', 'ONA', 'OBA', 'OAV']


class AnimeFile:
    """Anime File Data Class"""

    def __init__(self, anime_path: Path):
        log.debug(f"Try find data for video {anime_path}")
        if anime_path.suffix in VIDEO_FORMATS:
            for anime_regexp in config.REGEXPS_ANIME_DATA:
                log.debug(f"Try regexp: {anime_regexp}")
                match = re.search(anime_regexp, anime_path.name)
                if match:
                    log.info(f"Found anime data by regexp: {anime_regexp} for file {anime_path}")
                    self.path = anime_path
                    self.name = re.sub(r'_', ' ', match.group('title'))
                    self.extension = match.group('ext')
                    self.episode = int(match.group('episode') or -1)
                    self.season = int(match.group('season') or 1) if match.group('season') not in SEASON_SPECIALS else 0

                    return
            raise ValueError(f"The given path {anime_path} is not recognized by regexps")
        else:
            raise ValueError(f"The given path {anime_path} is not a supported video file")

    def __repr__(self):
        message = f"{self.name}.{self.extension}"
        if self.season is not None and self.episode != -1:
            message = f"{self.name} s{self.season:02}e{self.episode:02}.{self.extension}"

        return message
