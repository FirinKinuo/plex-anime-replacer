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

    def __init__(self, path: Path, name: str, extension: str, episode: int, season: Union[str, int]):
        self.path = path
        self.name = name
        self.extension = extension
        self.episode = episode
        self.season = season

    def __repr__(self):
        message = f"{self.name}.{self.extension}"
        if self.season is not None and self.episode != -1:
            message = f"{self.name} s{self.season:02}e{self.episode:02}.{self.extension}"

        return message


class DownloadedAnime:
    def __init__(self, path: Path):
        self.path = path

    def __repr__(self):
        return f"<Downloaded anime at {self.path}>"

    def search_metadata(self) -> AnimeFile:
        """
        Search for video metadata in name

        Returns:
           AnimeFile - Object AnimeFile
        """

        if self.path.suffix in VIDEO_FORMATS:
            log.debug(f"Try find data for video {self.path}")

            for anime_regexp in config.REGEXPS_ANIME_DATA:
                log.debug(f"Try regexp: {anime_regexp}")
                match = re.search(anime_regexp, self.path.name)
                if match:
                    log.info(f"Found anime data by regexp: {anime_regexp} for file {self.path}")
                    return AnimeFile(
                        path=self.path,
                        name=re.sub(r'_', ' ', match.group('title')),
                        extension=match.group('ext'),
                        episode=int(match.group('episode') or -1),
                        season=int(match.group('season') or 1) if match.group('season') not in SEASON_SPECIALS else 0
                    )
