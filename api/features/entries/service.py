from .repository import EntryRepository
from uuid import UUID
from typing import Annotated
from fastapi import Depends
from api.db.session import SessionDep
from .schemas import EntryCreate
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.models import Entry
from .exceptions import EntryNotFoundError
from pydantic import JsonValue


class EntryService():
    def __init__(self, repository: EntryRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def get(self, entry_id: UUID) -> Entry:
        entry = await self.repository.get(entry_id)
        if entry is None:
            raise EntryNotFoundError(f"Entry {entry_id} does not exist.")
        return entry

    async def list(self) -> list[Entry]:
        entries = await self.repository.list()
        return entries

    async def create(self, payload: EntryCreate) -> Entry:
        entry = await self.repository.create(payload.provider, payload.payload)
        await self.session.commit()
        return entry

    async def delete(self, entry_id: UUID) -> None:
        entry = await self.get(entry_id)
        if entry is None:
            raise EntryNotFoundError(f"Entry {entry_id} does not exist.")
        await self.repository.delete(entry)
        await self.session.commit()

    async def patch_payload(self, entry_id: UUID, payload_changes: dict[str, JsonValue]) -> Entry:
        entry = await self.get(entry_id)
        await self.repository.patch_payload(entry, payload_changes)
        await self.session.commit()
        return entry


def get_entry_service(session: SessionDep) -> EntryService:
    repository = EntryRepository(session)
    return EntryService(repository, session)


EntryServiceDep = Annotated[EntryService, Depends(get_entry_service)]