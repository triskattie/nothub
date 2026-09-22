from fastapi import APIRouter, HTTPException, status
from .schemas import EntryResponse, EntryCreate
from uuid import UUID
from .service import EntryServiceDep
from api.features.entries.service import EntryNotFound


router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: UUID, service: EntryServiceDep):
    try:
        return await service.get(entry_id)
    except EntryNotFound as exception:
        raise HTTPException(status_code=exception.status_code, detail=exception.detail)

@router.get("", response_model=list[EntryResponse])
async def list_entries(service: EntryServiceDep):
    return await service.list()

@router.post("", response_model=EntryResponse, status_code=201)
async def create_entry(payload: EntryCreate, service: EntryServiceDep):
    return await service.create(payload)

@router.delete("/{entry_id}", response_model=None, status_code=204)
async def delete_entry(entry_id: UUID, service: EntryServiceDep):
    try:
        return await service.delete(entry_id)
    except EntryNotFound as exception:
        raise HTTPException(status_code=exception.status_code, detail=exception.detail)