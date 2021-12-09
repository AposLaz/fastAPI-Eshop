from typing import List, Optional, Set
from pydantic import BaseModel, Field, validator

class Create_Items_Schema(BaseModel):
    name: str = Field(...,description="The name of food") # ... = require
    type: str
    description: Optional[str] = "No description"
    tags: List[str] = Field(...,description="Materials which used for food") 
    price: float
    available: Optional[bool] = Field(True, description="It says if food is available or not")
    inventory: Optional[int] = Field(0,description=" How many products exist in store ")

class Items_Schema(Create_Items_Schema):
    owner_id: int
            
# ** TAGS ** should not repeat, they would probably be unique strings so we use Set().
#With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.

#for Field = https://pydantic-docs.helpmanual.io/usage/schema/#field-customisation

