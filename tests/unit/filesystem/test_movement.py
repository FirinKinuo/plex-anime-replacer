import pytest

from replacer.filesystem import anime, movement
from tests import consts


@pytest.fixture()
def get_anime_data():
    downloads_folder = consts.DOWNLOADED_ANIME_FOLDER

    for anime_folder in downloads_folder.rglob("Fantasy Bishoujo *"):
        downloaded_anime = anime.DownloadedAnime(directory=anime_folder)
        return downloaded_anime.search_videos()


def test_move_anime_to_plex(get_anime_data):
    anime_files = get_anime_data

    for anime_file in anime_files:
        movement.move_anime_to_plex(anime_file=anime_file)
