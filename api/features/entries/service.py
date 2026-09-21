from .repository import EntryRepository
from uuid import UUID
from typing import Annotated
from fastapi import Depends
from api.db.session import SessionDep
from .schemas import EntryCreate
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.models import Entry

class EntryNotFound(Exception):
    status_code = 404
    detail = "Entry not found"

class NoEntriesFound(Exception):
    status_code = 404
    detail = "No entries found"


class EntryService():
    def __init__(self, repository: EntryRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def get(self, entry_id: UUID) -> Entry:
        entry = await self.repository.get(entry_id)
        if entry is None:
            raise EntryNotFound()
        return entry

    async def list(self) -> list[Entry]:
        entries = await self.repository.list()
        if entries is None:
            raise NoEntriesFound()
        return entries

    async def create(self, payload: EntryCreate) -> Entry:
        entry = await self.repository.create(payload.provider, payload.payload)
        await self.session.commit()
        return entry

    async def delete(self, entry_id: UUID) -> None:
        entry = await self.get(entry_id)
        await self.repository.delete(entry)
        await self.session.commit()


def get_entry_service(session: SessionDep) -> EntryService:
    repository = EntryRepository(session)
    return EntryService(repository, session)


EntryServiceDep = Annotated[EntryService, Depends(get_entry_service)]