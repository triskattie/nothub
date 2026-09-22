import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.models import Entry
from uuid import uuid4


# Happy paths

@pytest.mark.anyio
async def test_create_entry_when_input_is_valid_persists_entry_and_returns_201(client, db_session: AsyncSession):
    response = await client.post("/entries", json={"provider": "internal", "payload": {"type": "idea"}})

    assert response.status_code == 201

    result = await db_session.execute(
        select(Entry).where(Entry.provider == "internal")
    )
    entry = result.scalar_one()

    assert entry.payload == {"type": "idea"}

    body = response.json()

    assert body["id"] == str(entry.id)
    assert body["provider"] == entry.provider
    assert body["payload"] == entry.payload
    assert body["created_at"] is not None

@pytest.mark.anyio
async def test_get_entry_when_entry_exists_returns_entry_and_200(client, db_session: AsyncSession):
    entry = Entry(
        provider="internal",
        payload={"test": "testcontent"}
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    response = await client.get(f"/entries/{entry.id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == str(entry.id)
    assert body["provider"] == entry.provider
    assert body["payload"] == entry.payload
    assert body["created_at"] is not None

@pytest.mark.anyio
async def test_delete_entry_when_entry_exists_removes_entry_and_returns_204(client, db_session: AsyncSession):
    entry = Entry(
        provider="internal",
        payload={"test": "testcontent"}
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    response = await client.delete(f"/entries/{entry.id}")

    assert response.status_code == 204
    assert response.content == b""

    result = await db_session.execute(
        select(Entry).where(Entry.id == entry.id)
    )

    assert result.scalar_one_or_none() is None

@pytest.mark.anyio
async def test_list_entries_when_no_entries_returns_empty_array_and_200(client):
    response = await client.get("/entries")

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.anyio
async def test_list_entries_when_entries_exist_returns_entries_and_200(client, db_session: AsyncSession):
    entry1 = Entry(
        provider="internal",
        payload={"test1": "testcontent1"}
    )
    entry2 = Entry(
        provider="internal",
        payload={"test2": "testcontent2"}
    )
    db_session.add_all([entry1, entry2])
    await db_session.commit()
    await db_session.refresh(entry1)
    await db_session.refresh(entry2)

    response = await client.get("/entries")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    entries_by_id = {item["id"]: item for item in body}
    response_entry1 = entries_by_id[str(entry1.id)]
    response_entry2 = entries_by_id[str(entry2.id)]

    assert response_entry1["provider"] == entry1.provider
    assert response_entry1["payload"] == entry1.payload
    assert response_entry2["provider"] == entry2.provider
    assert response_entry2["payload"] == entry2.payload

# Error paths


@pytest.mark.anyio
async def test_create_entry_with_invalid_payload_returns_422(client):
    response = await client.post("/entries", json={"porvider": "internal", "payload": {"type": "idea"}})

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_entry_when_entry_does_not_exist_returns_404(client):
    missing_id = uuid4()
    response = await client.get(f"/entries/{missing_id}")

    assert response.status_code == 404

@pytest.mark.anyio
async def test_delete_entry_when_entry_does_not_exist_returns_404(client):
    missing_id = uuid4()
    response = await client.delete(f"/entries/{missing_id}")

    assert response.status_code == 404

@pytest.mark.anyio
async def test_get_entry_with_invalid_uuid_returns_422(client):
    response = await client.get(f"/entries/1")

    assert response.status_code == 422

@pytest.mark.anyio
async def test_delete_entry_with_invalid_uuid_returns_422(client):
    response = await client.delete(f"/entries/1")

    assert response.status_code == 422