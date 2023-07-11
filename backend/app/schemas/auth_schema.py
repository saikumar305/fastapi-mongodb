from uuid import UUID
from typing import Optional
from pydantic   import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: UUID
    exp: int