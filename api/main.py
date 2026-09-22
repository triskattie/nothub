from fastapi import FastAPI
from .features.entries.router import router as entry_router


app = FastAPI()


@app.get("/")
def root():
    return {"Hello, world!"}

app.include_router(entry_router)
