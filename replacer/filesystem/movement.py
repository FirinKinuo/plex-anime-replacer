from shutil import copyfile
from pathlib import Path
from typing import Union
from logging import getLogger

from replacer.settings import config
from replacer.filesystem import anime

log = getLogger(__name__)


def move_anime_to_plex(anime_file: Union[anime.AnimeFile, anime.AnimeSerialFile]):
    plex_folder = config.DIR_PLEX_ANIME_LIBRARY
    anime_folder = Path(plex_folder, anime_file.name)
    new_anime_file = f"{anime_file.name} s{anime_file.season:}e{anime_file.episode}.{anime_file.extension}" \
        if isinstance(anime_file, anime.AnimeSerialFile) else f"{anime_file.name}.{anime_file.extension}"
    log.info(f"Rename anime file {anime_file.path} to {new_anime_file}")

    if not anime_folder.exists():
        log.info(f"Create folder for anime {anime_file.name}")
        anime_folder.mkdir(parents=True)

    if not Path(anime_folder, new_anime_file).exists():
        log.info(f"Copy attempt {new_anime_file} to folder {anime_folder}")
        copyfile(src=anime_file.path, dst=Path(anime_folder, new_anime_file))
