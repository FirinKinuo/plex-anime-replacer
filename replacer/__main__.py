import argparse

from pathlib import Path
from logging import getLogger

from replacer.filesystem import anime, movement

log = getLogger(__name__)


def init_args_parser() -> argparse.Namespace:
    """
    Argument parsing initialization when called from the command line

    Returns:
        argparse.Namespace: Namespace argument
    """
    parser = argparse.ArgumentParser(description='Replace anime from FunDub trackers folder to plex with rename')
    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        dest="path",
        help="Path to Anime folder",
        metavar="path/anime/folder",
        required=True
    )

    return parser.parse_args()


def replace_all_anime_in_folder(anime_folder_path: Path):
    """
    Move all the anime in the folder to the Plex library directory
    With a Plex-appropriate name replacement
    Args:
        anime_folder_path: pathlib.Path - The path in the pathlib format to the anime folder
    """
    downloaded_anime = anime.DownloadedAnime(directory=anime_folder_path)
    for anime_file in downloaded_anime.search_videos():
        try:
            movement.move_anime_to_plex(anime_file=anime_file)
        except PermissionError:
            log.critical("Unable to move file, check permissions")


if __name__ == "__main__":
    args = init_args_parser()

    replace_all_anime_in_folder(anime_folder_path=args.path)
