from pydantic import BaseModel, ConfigDict, JsonValue
from uuid import UUID
from datetime import datetime

class EntryCreate(BaseModel):
    provider: str
    payload: dict[str, JsonValue]

class EntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    provider: str
    payload: dict[str, JsonValue]
    created_at: datetime