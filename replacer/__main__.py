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

    parser.add_argument(
        "--use_symlink",
        dest="use_symlink",
        help="Use symlink instead of copy (Faster, but may not work on all OS)",
        action='store_true',
        required=False
    )

    return parser.parse_args()


def replace_anime_file(anime_file_path: Path, *args, **kwargs):
    """
    Move the specified anime file to the Plex library directory
    With a Plex-appropriate name replacement

    Args:
        anime_file_path: pathlib.Path - The path in the pathlib format to the anime file

    Keyword Args:
        save_original: bool - Keep original file when transferring? (Faster if not save)
        use_symlink: bool - Use symlink instead of copy (Faster, but may not work on all OS)
    """
    if anime_file_path.exists() and anime_file_path.suffix in anime.VIDEO_FORMATS:
        downloaded_anime = anime.DownloadedAnime(path=anime_file_path)
        try:
            movement.move_anime_to_plex(anime_file=downloaded_anime.search_metadata(), save_original=save_original)
        except PermissionError:
            log.critical("Unable to move file, check permissions")


if __name__ == "__main__":
    opts = init_args_parser()
    if opts.path.exists():
        if opts.path.is_dir():
            for anime_file in opts.path.rglob("*"):
                replace_anime_file(anime_file_path=opts.path,
                                   save_original=opts.save_original,
                                   use_symlink=opts.use_symlink)
        else:
            replace_anime_file(anime_file_path=opts.path,
                               save_original=opts.save_original,
                               use_symlink=opts.use_symlink)
