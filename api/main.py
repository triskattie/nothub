import os

from fastapi import FastAPI
from .features.entries.router import router as entry_router
from api.core.exception_handlers import register_exception_handlers

app = FastAPI()

APP_VERSION = os.getenv("APP_VERSION")


@app.get("/")
def root():
    return {"Hello, world!"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}

register_exception_handlers(app)

app.include_router(entry_router)
