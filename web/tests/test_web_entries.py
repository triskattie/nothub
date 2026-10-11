import pytest
from uuid import uuid4


@pytest.mark.anyio
async def test_edit_entry_updates_only_changed_field(web_client, api_client, api_entry):
    response = await web_client.post(
        f"/entries/{api_entry['id']}/edit",
        data={
            "title": "updated title",
            "description": "original description",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303

    response = await api_client.get(f"/entries/{api_entry['id']}")
    response.raise_for_status()
    assert response.json()["payload"] == {
        "title": "updated title",
        "description": "original description",
    }

@pytest.mark.anyio
async def test_create_entry_creates_entry(web_client):
    create_response = await web_client.post(
        "/entries/create",
        data={
            "title": "test title",
            "description": "test description",
        },
        follow_redirects=False,
    )

    assert create_response.status_code == 303

@pytest.mark.anyio
async def test_delete_entry_deletes_entry(web_client, api_client, api_entry):
    entry_id = api_entry["id"]
    response = await web_client.post(f"/entries/{entry_id}/delete", follow_redirects=False)

    assert response.status_code == 303

    check_response = await api_client.get(f"/entries/{entry_id}")

    assert check_response.status_code == 404