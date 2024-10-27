import uuid

from pydantic import BaseModel


class RequestCheckDuplicateSchema(BaseModel):
    link: str


class ResponseCheckDuplicateSchema(BaseModel):
    is_duplicate: bool
    duplicate_for: uuid.UUID
