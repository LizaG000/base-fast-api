from fastapi import FastAPI
from src.main.config import config
from src.presentation.fastapi.setup import setup_routes

app = FastAPI(
    title=config.api.project_name
)

setup_routes(app, config)
