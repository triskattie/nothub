from fastapi import FastAPI
from .features.entries.router import router as entry_router
from api.core.exception_handlers import register_exception_handlers

app = FastAPI()


@app.get("/")
def root():
    return {"Hello, world!"}

register_exception_handlers(app)

app.include_router(entry_router)
