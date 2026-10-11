from .repository import EntryRepository
from uuid import UUID
from typing import Annotated
from fastapi import Depends
from api.db.session import SessionDep
from .schemas import EntryCreate, EntryPatch
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
        entry = await self.repository.create(payload.provider, payload.payload, payload.type)
        await self.session.commit()
        return entry

    async def delete(self, entry_id: UUID) -> None:
        entry = await self.get(entry_id)
        await self.repository.delete(entry)
        await self.session.commit()

    async def patch(self, entry_id: UUID, patch: EntryPatch) -> Entry:
        entry = await self.get(entry_id)
        changes = patch.model_dump(exclude_unset=True)

        if "type" in changes:
            entry.type = changes["type"]

        if "payload" in changes and changes.get("payload") is not None:
            old_payload = entry.payload.copy()
            old_payload.update(changes["payload"])
            entry.payload = old_payload

        await self.session.commit()
        return entry


def get_entry_service(session: SessionDep) -> EntryService:
    repository = EntryRepository(session)
    return EntryService(repository, session)


EntryServiceDep = Annotated[EntryService, Depends(get_entry_service)]