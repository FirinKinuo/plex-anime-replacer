import pytest

from pathlib import Path

from replacer.filesystem import anime


from tests import consts
from tests.generators import random_string as rndstr
from tests.unit.filesystem import AnimeProviders, AnimeFileType
from tests.unit.filesystem.fixtures import *


def test_downloaded_anime_repr():
    path_payload = Path(consts.DOWNLOADED_ANIME_FOLDER, rndstr(12))

    downloaded_anime = anime.DownloadedAnime(path=path_payload)

    assert isinstance(downloaded_anime, anime.DownloadedAnime)
    assert str(downloaded_anime) == f"<Downloaded anime at {path_payload}>"


@pytest.mark.parametrize("anime_provider", (AnimeProviders.ANILIBRIA,))
@pytest.mark.parametrize(
    "file_type,season",
    ((AnimeFileType.SERIAL, False),
     (AnimeFileType.SERIAL, True),
     (AnimeFileType.SPECIAL, False),
     (AnimeFileType.FUll_LENGTH, False)))
def test_search_anime(generate_anime_file, anime_provider, file_type, season):
    anime_metadata = generate_anime_file(provider=anime_provider, file_type=file_type, season=season)

    downloaded_anime = anime.DownloadedAnime(path=anime_metadata['path'])

    anime_file = downloaded_anime.search_metadata()

    assert isinstance(anime_file, anime.AnimeFile)

    if file_type in (AnimeFileType.SERIAL, AnimeFileType.SPECIAL):
        assert anime_file.path == anime_metadata['path']
        assert anime_file.name == anime_metadata['name'].replace('_', ' ')

        if file_type == AnimeFileType.SERIAL:
            assert anime_file.season == int(anime_metadata['season'])
        elif file_type == AnimeFileType.SPECIAL:
            assert anime_file.season == 0

        assert anime_file.episode == anime_metadata['episode']
        assert anime_file.extension == anime_metadata['extension']

        if file_type == AnimeFileType.SERIAL:
            assert str(anime_file) == f"{anime_metadata['name'].replace('_', ' ')} " \
                                      f"s{int(anime_metadata['season']):02}e{anime_metadata['episode']:02}." \
                                      f"{anime_metadata['extension']}"
        elif file_type == AnimeFileType.SPECIAL:
            assert str(anime_file) == f"{anime_metadata['name'].replace('_', ' ')} " \
                                      f"s00e{anime_metadata['episode']:02}.{anime_metadata['extension']}"

    elif file_type == AnimeFileType.FUll_LENGTH:
        assert anime_file.path == anime_metadata['path']
        assert anime_file.name == anime_metadata['name'].replace('_', ' ')
        assert anime_file.extension == anime_metadata['extension']

        assert str(anime_file) == f"{anime_metadata['name'].replace('_', ' ')}.{anime_metadata['extension']}"
