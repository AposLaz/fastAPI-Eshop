from pydantic import BaseModel
from pydantic.fields import Field


class Votes_Schema(BaseModel):
    
    item_id: int
    like: int = Field(0,le=1)               #default value = 0, and value can be obly "1 = like" or "0 = dislike"

