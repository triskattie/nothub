from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api.db.models import Entry
from typing import Any
from sqlalchemy import select


class EntryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, entry_id: UUID):
        return await self.session.get(Entry, entry_id)

    async def list(self) -> list[Entry]:
        stmt = select(Entry)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def create(self, provider: str, payload: dict[str, Any]):
        entry = Entry(
            provider=provider,
            payload=payload
        )
        self.session.add(entry)
        await self.session.flush()
        await self.session.refresh(entry)
        return entry

    async def delete(self, entry: Entry) -> None:
        await self.session.delete(entry)