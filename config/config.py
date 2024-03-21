import os
from pathlib import Path
from typing import Union

import yaml
from sqlalchemy import create_engine

import animal_logger
from config.log_config import LOGGER

class Config:

    DEFAULT_DB_CONFIG_FILE = Path(animal_logger.__file__).parent.parent / 'config/db_config.yaml'
    _DB_URL = None
    _CONFIG_DICT = None
    
    def __init__(self, db_config_file: Union[str, Path] = DEFAULT_DB_CONFIG_FILE) -> None:
        Config._CONFIG_DICT = self._load_db_config(db_config_file)
    
    @staticmethod
    def _load_db_config(db_config_file: Union[str, Path]) -> None:
        with open(db_config_file, 'rb') as f:
            db_config_file = yaml.safe_load(f)
        return db_config_file
    
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
