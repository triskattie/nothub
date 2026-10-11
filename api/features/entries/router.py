from fastapi import APIRouter
from .schemas import EntryResponse, EntryCreate, EntryPayloadPatch
from uuid import UUID
from .service import EntryServiceDep


router = APIRouter(prefix="/entries", tags=["entries"])


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: UUID, service: EntryServiceDep):
    return await service.get(entry_id)

@router.get("", response_model=list[EntryResponse])
async def list_entries(service: EntryServiceDep):
    return await service.list()

@router.post("", response_model=EntryResponse, status_code=201)
async def create_entry(payload: EntryCreate, service: EntryServiceDep):
    return await service.create(payload)

@router.delete("/{entry_id}", response_model=None, status_code=204)
async def delete_entry(entry_id: UUID, service: EntryServiceDep):
    return await service.delete(entry_id)

@router.patch("/{entry_id}/payload", response_model=EntryResponse)
async def patch_entry_payload(entry_id: UUID, patch: EntryPayloadPatch, service: EntryServiceDep):
    return await service.patch_payload(entry_id, patch.fields)