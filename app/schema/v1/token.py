from typing import Optional
from pydantic import BaseModel

class Token_Schema(BaseModel):
    access_token: str
    refresh_token: str

class Token_Data_Schema(BaseModel):
    id: Optional[str] = None