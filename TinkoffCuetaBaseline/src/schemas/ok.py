from pydantic import BaseModel


class StatusSchema(BaseModel):
    status: str
