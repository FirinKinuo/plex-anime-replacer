import os
import shutil
from pathlib import Path
from logging import getLogger

from replacer.settings import config
from replacer.filesystem import anime

log = getLogger(__name__)


def move_anime_to_plex(anime_file: anime.AnimeFile, *args, **kwargs) -> Path:
    """

    Args:
        anime_file: The path in the pathlib format to the anime file

    Keyword Args:
        save_original: bool - Keep original file when transferring? (Faster if not save)
        use_symlink: bool - Use symlink instead of copy (Faster, but may not work on all OS)
    Returns:
        Path - New anime file path
    """
    plex_folder = config.DIR_PLEX_ANIME_LIBRARY
    anime_folder = Path(plex_folder, anime_file.name)
    new_anime_file = Path(anime_folder, str(anime_file))

    log.info(f"Rename anime file {anime_file.path} to {anime_file}")

    if not anime_folder.exists():
        log.info(f"Create folder for anime {anime_file.name}")
        anime_folder.mkdir(parents=True)

    if not new_anime_file.exists():
        if kwargs.get('save_original'):
            if kwargs.get('use_symlink'):
                log.info(f"Attempt to create {anime_folder} symlink for {anime_file}")
                os.symlink(src=anime_file.path, dst=new_anime_file)
            else:
                log.info(f"Copy attempt {anime_file} to folder {anime_folder}")
                shutil.copy2(src=anime_file.path, dst=new_anime_file)
        else:
            log.info(f"Replace attempt {anime_file} to folder {anime_folder}")
            shutil.move(src=anime_file.path, dst=new_anime_file)

    return new_anime_file
