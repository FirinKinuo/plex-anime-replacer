import pytest

from pathlib import Path

from replacer.filesystem import anime

from tests import consts


def test_search_videos():
    downloads_folder = consts.DOWNLOADED_ANIME_FOLDER

    for anime_folder in downloads_folder.rglob("*]"):
        downloaded_anime = anime.DownloadedAnime(directory=anime_folder)
        assert isinstance(downloaded_anime.search_videos(), list)

    