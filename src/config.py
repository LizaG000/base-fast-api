import os
from pydantic import ConfigDict
from dynaconf import Dynaconf
from loguru import logger

from src.application.schemas.common import BaseSchema


class ApiConfig(BaseSchema):
    host: str = 'localhost'
    port: int = 8000
    project_name: str = 'base'

class Config(BaseSchema):
    model_config = ConfigDict(extra='allow', from_attributes=True)
    api: ApiConfig


def get_config() -> Config:
    dynaconf = Dynaconf(
        settings_files=[
            './deploy/configs/config.toml'
        ],
        envvar_prefix='Liza',
        load_dotenv=True,
    )
    logger.info(dynaconf.api)
    return Config.model_validate(dynaconf)