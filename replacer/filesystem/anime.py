import re
from pathlib import Path
from logging import getLogger

from replacer.settings import config

log = getLogger(__name__)

VIDEO_FORMATS = [
    '.3gp', '.asf', '.avi', '.flv', '.m2ts', '.m4v', '.mkv',
    '.mov', '.mp4', '.mts', '.ogg', '.vob', '.wmv', '.webm'
]


class AnimeFile:
    """Anime File Data Class"""

    def __init__(self, path: Path, name: str, extension: str):
        self.path = path
        self.name = name
        self.extension = extension

    def __repr__(self):
        return f"{self.name}"


class AnimeSerialFile(AnimeFile):
    def __init__(self, episode: int, season: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.episode = episode
        self.season = season

    def __repr__(self):
        return f"{self.name} s{self.season:02}e{self.episode:02}"


class DownloadedAnime:
    def __init__(self, directory: Path):
        self.directory = directory
        self.videos = []

    def search_videos(self) -> list[AnimeFile]:
        """
        Search for video files in a directory

        Returns:
            list[AnimeFile] - List of objects AnimeFile
        """
        video_files = (file for file in self.directory.rglob('*') if file.suffix in VIDEO_FORMATS)
        anime_files = []

        for anime_video in video_files:
            log.debug(f"Try find data for video {anime_video}")
            for anime_regexp in config.REGEXPS_ANIME_DATA:
                log.debug(f"Try regexp: {anime_regexp}")
                match = re.search(anime_regexp, anime_video.name)
                if match:
                    log.info(f"Found anime data by regexp: {anime_regexp} for file {anime_video}")
                    anime_files.append(AnimeSerialFile(
                        path=anime_video,
                        name=re.sub(r'_', ' ', match.group('title')),
                        extension=match.group('ext'),
                        episode=int(match.group('episode')),
                        season=int(match.group('season') or 1)
                    ) if match.group('episode') else AnimeFile(path=anime_video,
                                                               name=re.sub(r'_', ' ', match.group('title')),
                                                               extension=match.group('ext')))
                    break

        return anime_files
