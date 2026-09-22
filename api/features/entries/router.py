from fastapi import APIRouter
from .schemas import EntryResponse, EntryCreate
from uuid import UUID
from .service import EntryServiceDep


router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: UUID, service: EntryServiceDep):
    return await service.get(entry_id)

@router.get("", response_model=list[EntryResponse])
async def list_entries(service: EntryServiceDep):
    return await service.list()

@router.post("", response_model=EntryResponse)
async def create_entry(payload: EntryCreate, service: EntryServiceDep):
    return await service.create(payload)

@router.delete("/{entry_id}", response_model=None)
async def delete_entry(entry_id: UUID, service: EntryServiceDep):
    return await service.delete(entry_id)