import pytest

from replacer.filesystem import anime, movement
from tests.unit.filesystem import AnimeProviders, AnimeFileType
from tests.unit.filesystem.fixtures import *


@pytest.mark.parametrize("anime_provider", (AnimeProviders.ANILIBRIA,))
@pytest.mark.parametrize('save_original', (True, False))
def test_move_anime_to_plex_copy_mode(generate_anime_file, anime_provider, save_original):
    generated_file = generate_anime_file(provider=anime_provider, file_type=AnimeFileType.SERIAL, season=False)
    anime_file = anime.AnimeFile(generated_file['path'])

    moved_anime = movement.move_anime_to_plex(anime_file=anime_file,
                                              save_original=save_original)

    assert moved_anime.exists()
    assert anime_file.path.exists() if save_original else not anime_file.path.exists()
