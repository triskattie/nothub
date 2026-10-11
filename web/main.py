from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from datetime import datetime
from uuid import UUID
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="web/templates")

app.mount("/static", StaticFiles(directory="web/static"), name="static")

@app.get("/")
async def index(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get("http://api:8000/entries") # TODO: CHANGE THIS TO ENV VARIABLE
        response.raise_for_status()
        entries = response.json()

        version_response = await client.get("http://api:8000/version") # TODO: CHANGE THIS TO ENV VARIABLE
        version_response.raise_for_status()
        version = version_response.json()["version"]

    # Make the datetime readable instead of something like 2026-10-09T19:35:06.148548, it will be something like 09/10/2026 19:35
    for entry in entries:
        entry["created_at"] = datetime.fromisoformat(entry["created_at"]).strftime("%d/%m/%Y %H:%M")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "entries": entries,
            "version": version
        }
    )

@app.post("/entries/{entry_id}/delete")
async def delete_entry(entry_id: UUID):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://api:8000/entries/{entry_id}")

    if response.status_code == 404:
        raise HTTPException(status_code=404) # TODO: EITHER REMOVE THIS OR MAKE IT BETTER

    response.raise_for_status()

    return RedirectResponse(
        url="/",
        status_code=303 # TODO: ADD DETAIL?
    )

@app.post("/entries/create")
async def create_entry(title: str = Form(...), description: str = Form(...)):
    entry = {
        "provider": "web",
        "payload": {
            "title": title,
            "description": description
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("http://api:8000/entries", json=entry)

    response.raise_for_status()

    return RedirectResponse(
        url="/",
        status_code=303 # TODO: ADD DETAIL?
    )

@app.get("/entries/{entry_id}/edit")
async def edit_entry_page(entry_id: UUID, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api:8000/entries/{entry_id}") # TODO: MAKE THIS AN ENV VARIABLE
        response.raise_for_status()
        entry = response.json()

        version_response = await client.get("http://api:8000/version") # TODO: CHANGE THIS TO ENV VARIABLE
        version_response.raise_for_status()
        version = version_response.json()["version"]

    return templates.TemplateResponse(
        request=request,
        name="edit_entry.html",
        context={
            "entry": entry,
            "version": version
        }
    )

@app.post("/entries/{entry_id}/edit")
async def edit_entry(entry_id: UUID, title: str = Form(...), description: str = Form(...)):
    async with httpx.AsyncClient() as client:
        original_response = await client.get(f"http://api:8000/entries/{entry_id}") # TODO: MAKE THIS AN ENV VARIABLE
        original_response.raise_for_status()
        original = original_response.json()["payload"]

        changed_fields = {}
        if title != original["title"]:
            changed_fields["title"] = title

        if description != original["description"]:
            changed_fields["description"] = description

        if changed_fields:
            response = await client.patch(f"http://api:8000/entries/{entry_id}", json={"payload": changed_fields})
            response.raise_for_status()

    return RedirectResponse(
        url="/",
        status_code=303
    )
