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
        help="Path to Anime folder or file",
        metavar="path/anime/folder/file",
        required=True
    )
    parser.add_argument(
        "--save-original",
        dest="save_original",
        help="Keep the original file (slower)",
        action='store_true',
        required=False
    )

    return parser.parse_args()


def replace_anime_file(anime_file_path: Path, save_original: bool = True):
    """
    Move the specified anime file to the Plex library directory
    With a Plex-appropriate name replacement

    Args:
        anime_file_path: pathlib.Path - The path in the pathlib format to the anime file
        save_original: bool - default: True - Keep original file when transferring? (Faster if not save)
    """
    if anime_file_path.exists() and anime_file_path.suffix in anime.VIDEO_FORMATS:
        downloaded_anime = anime.DownloadedAnime(path=anime_file_path)
        try:
            movement.move_anime_to_plex(anime_file=downloaded_anime.search_metadata(), save_original=save_original)
        except PermissionError:
            log.critical("Unable to move file, check permissions")


def replace_all_anime_in_folder(anime_folder_path: Path, save_original: bool = True):
    """
    Move all the anime in the folder to the Plex library directory
    With a Plex-appropriate name replacement

    Args:
        anime_folder_path: pathlib.Path - The path in the pathlib format to the anime folder
        save_original: bool - default: True - Keep original file when transferring? (Faster if not save)
    """
    for anime_file in anime_folder_path.rglob("*"):
        replace_anime_file(anime_file_path=anime_file, save_original=save_original)


if __name__ == "__main__":
    args = init_args_parser()
    if args.path.exists():
        if args.path.is_dir():
            replace_all_anime_in_folder(anime_folder_path=args.path, save_original=args.save_original)
        else:
            replace_anime_file(anime_file_path=args.path, save_original=args.save_original)
