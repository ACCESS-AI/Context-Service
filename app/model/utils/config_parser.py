import yaml
from pydantic import BaseModel
from typing import Dict, Optional
import yaml
import os

from app.model.utils.constants import CONFIG_PATH

class EmbedderConfig(BaseModel):
    name: str

class VectorstoreConfig(BaseModel):
    name: str


class AppConfig(BaseModel):
    embedder: EmbedderConfig
    vectorstore: VectorstoreConfig

class ConfigParser:

    def __init__(self,config_path:str = CONFIG_PATH) -> None:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.__config = AppConfig(**config)


    @property
    def embedder_config(self) -> EmbedderConfig:
        return self.__config.embedder
    
    @property
    def vectorstore_config(self) -> VectorstoreConfig:
        return self.__config.vectorstore
    
