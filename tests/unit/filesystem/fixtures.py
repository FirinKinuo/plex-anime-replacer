import shutil

import pytest

from pathlib import Path
from typing import Optional

from tests import consts
from tests.generators import random_int as rndint
from tests.generators import random_string as rndstr
from tests.unit.filesystem import AnimeProviders, AnimeFileType, AnimeMetaData

__all__ = ['prepare_testing_folders', 'generate_anime_file']


@pytest.fixture(scope="session")
def prepare_testing_folders():
    try:
        shutil.rmtree(consts.DOWNLOADED_ANIME_FOLDER)
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree(consts.TARGET_ANIME_FOLDER)
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def generate_anime_file(prepare_testing_folders) -> callable:
    def generate_anime_file_(provider: AnimeProviders,
                             file_type: AnimeFileType,
                             season: Optional[bool]) -> AnimeMetaData:
        anime_dir = Path(consts.DOWNLOADED_ANIME_FOLDER, rndstr(12))
        anime_file = anime_dir

        if not anime_dir.exists():
            anime_dir.mkdir(parents=True)

        metadata = AnimeMetaData(
            path=Path(),
            name=f"{rndstr(6)}_{rndstr(6)}",
            extension='mkv',
            episode=rndint(2),
            season=str(rndint(2) if season else 1) if file_type == AnimeFileType.SERIAL else 'OVA'
        )

        if provider == AnimeProviders.ANILIBRIA:
            if file_type in (AnimeFileType.SERIAL, AnimeFileType.SPECIAL):
                anime_file = anime_dir.joinpath(
                    f"{metadata['name']}"
                    f"{'_' + metadata['season'] if season or file_type == AnimeFileType.SPECIAL else ''}_"
                    f"[{metadata['episode']}]_[AniLibria_TV].{metadata['extension']}")

            elif file_type == AnimeFileType.FUll_LENGTH:
                anime_file = anime_dir.joinpath(f"{metadata['name']}_[AniLibria_TV].{metadata['extension']}")

        if not anime_file.exists():
            anime_file.touch()
            metadata['path'] = anime_file

        return metadata

    return generate_anime_file_
