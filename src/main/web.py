from fastapi import FastAPI
from src.main.config import config

app = FastAPI(
    title=config.api.project_name,
    redoc_url=None,
    openapi_url=None,
    docs_url=None,
)