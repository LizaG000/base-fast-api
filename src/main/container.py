from dishka import make_async_container
from src.main.provider import MainProvider
from src.config import Config
from src.main.config import config

container = make_async_container(
    MainProvider(),
    context={
        Config: config
    }
)