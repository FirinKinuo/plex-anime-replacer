import sys
import logging

from pathlib import Path

import yaml

log = logging.getLogger('init')
EXTERNAL_FILES_DIR = Path('/etc', 'plex-anime-replacer')
YAML_CONFIG_PATH = Path(EXTERNAL_FILES_DIR, 'config.yaml')
IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # Если найдены пути тестов, то переходим в режим теста


def get_config_from_yaml() -> dict:
    """
    Получение конфигурации из файла .yaml

    Returns:
        (dict): Словарь с конфигурацией из .yaml файла
    """
    try:
        with open(YAML_CONFIG_PATH, 'r', encoding="utf-8") as config_file:
            return yaml.load(stream=config_file, Loader=yaml.loader.SafeLoader)
    except FileNotFoundError:
        error_message = f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}"
        raise SystemExit(error_message) from SystemExit


_config = get_config_from_yaml()

DEBUG = bool(_config.get('debug')) or False
LOG_LEVEL = logging.getLevelName(_config.get('log_level' if not DEBUG else 'debug').upper())
LOG_PATH = Path(_config.get('log_path') or '', 'replacer.log')

BACKUP_DIR = Path(_config.get('backup_dir')) if _config.get('backup_dir') else None

DIR_DOWNLOADED_ANIME = Path(_config.get('dir_downloaded_anime') if not IS_TEST else 'tests/testing_folders/downloads')
DIR_PLEX_ANIME_LIBRARY = Path(_config.get('dir_plex_anime_library') if not IS_TEST else 'tests/testing_folders/anime')

logging.basicConfig(level=LOG_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S",
                    filename=LOG_PATH if not DEBUG else None,
                    filemode='a')
