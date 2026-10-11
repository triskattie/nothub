from pydantic import BaseModel, ConfigDict, JsonValue
from uuid import UUID
from datetime import datetime

class EntryCreate(BaseModel):
    provider: str
    type: str | None = None
    payload: dict[str, JsonValue]

class EntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    provider: str
    type: str | None = None
    payload: dict[str, JsonValue]
    created_at: datetime

class EntryPatch(BaseModel):
    type: str | None = None
    payload: dict[str, JsonValue] | None = None