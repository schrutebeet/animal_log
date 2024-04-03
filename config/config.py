import os
from pathlib import Path
from typing import Union

import yaml
from sqlalchemy import create_engine

from config.log_config import LOGGER

class Config:

    DEFAULT_DB_CONFIG_FILE = Path(__file__).parent.parent / 'config/db_config.yaml'
    DEFAULT_APP_CONFIG_FILE = Path(__file__).parent.parent / 'config/app_config.yaml'
    _DB_URL = None
    _CONFIG_DICT = {}
    
    def __init__(self, 
                 db_config_path: Union[str, Path] = DEFAULT_DB_CONFIG_FILE,
                 app_config_path: Union[str, Path] = DEFAULT_APP_CONFIG_FILE) -> None:
        self._load_config_file(db_config_path)
        self._load_config_file(app_config_path)
    
    @staticmethod
    def _load_config_file(config_file: Union[str, Path]) -> None:
        with open(config_file, 'rb') as f:
                config_file = yaml.safe_load(f)
        Config._CONFIG_DICT.update(config_file)
    
    @staticmethod
    def get_info() -> dict:
        if Config._CONFIG_DICT:
                Config._CONFIG_DICT['user'] = os.getenv('USERNAME')
                Config._CONFIG_DICT['password'] = os.getenv('PASSWORD')
                Config._CONFIG_DICT['db_url'] = (
                                                    f"postgresql://{os.getenv('USERNAME')}:"
                                                    f"{os.getenv('PASSWORD')}@"
                                                    f"{Config._CONFIG_DICT['host']}/"
                                                    f"{Config._CONFIG_DICT['database']}"
                                                )
                Config._CONFIG_DICT['db_engine'] = create_engine(Config._CONFIG_DICT['db_url'])
        else:
            raise Exception("Attempting to fetch config info, but Config constructor has not been called yet.")
        return Config._CONFIG_DICT
