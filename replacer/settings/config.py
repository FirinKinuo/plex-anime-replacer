import sys
import logging

from pathlib import Path

import yaml

log = logging.getLogger('init')
EXTERNAL_FILES_DIR = Path('/etc', 'plex-anime-replacer')
YAML_CONFIG_PATH = Path(EXTERNAL_FILES_DIR, 'config.yaml')
IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # If test paths are found, then go to test mode


def get_config_from_yaml() -> dict:
    """
    Getting configuration from .yaml file
    Returns:
        dict - Dictionary with configuration from .yaml file
    """
    try:
        with open(YAML_CONFIG_PATH, 'r', encoding="utf-8") as config_file:
            return yaml.load(stream=config_file, Loader=yaml.loader.SafeLoader)
    except FileNotFoundError:
        error_message = f"Невозможно найти файл конфигурации! Путь: {YAML_CONFIG_PATH}"
        raise SystemExit(error_message) from SystemExit


_config = get_config_from_yaml()

DEBUG = bool(_config.get('debug')) or False
LOG_LEVEL = logging.getLevelName((_config.get('log_level') if not DEBUG else 'debug').upper())
LOG_PATH = Path(_config.get('log_path') or '', 'replacer.log')

BACKUP_DIR = Path(_config.get('backup_dir')) if _config.get('backup_dir') else None

DIR_PLEX_ANIME_LIBRARY = Path(_config.get('dir_plex_anime_library') if not IS_TEST else 'tests/testing_folders/anime')

REGEXPS_ANIME_DATA = _config.get('regexps_anime_data')

logging.basicConfig(level=LOG_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(funcName)s] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S",
                    filename=LOG_PATH if not DEBUG else None,
                    filemode='a')
