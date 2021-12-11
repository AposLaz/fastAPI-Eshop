from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from pydantic.fields import Field
from pydantic.networks import EmailStr
import phonenumbers
from sqlalchemy.sql.functions import user

#********************************************************************************** POST
class Users_Schema(BaseModel):
    username: str 
    password: str = Field(..., min_length=6)
    email: EmailStr
    telephone: str = Field(... ,min_length=10, max_length=10)

    @validator('telephone')
    def valid_phone(cls,v):
        assert str(v).isdecimal() , "This is invalid mobile number"
        return v


class Config:
        orm_mode = True
        #here we give an example of schema
        schema_extra = {
            "example":{
                "username":"ApLaz",
                "password": "password",
                "email": "aplazidis@gmail.com",
                "telephone": "6979977872"   
            }
        }


class Create_Users_Schema(Users_Schema):
    
    password2: str = Field(...,min_length=6)

    @validator('password2')
    def valid_password(cls,v,values,**kwargs):
        if 'password' in values and v!= values['password']:
            raise ValueError("Passwords do not match")
        return v

#************************************************************************* UPDATE

class Update_User_Schema(BaseModel):
    username: Optional[str]
    password: Optional[str] = Field(None ,min_length=6)
    email: Optional[EmailStr]
    telephone: Optional[str] = Field(None, min_length=10, max_length=10)

    @validator('telephone')
    def valid_phone(cls, v):
        assert str(v).isdecimal(), 'This is invalid phone number'
        phone = "+30-"+v
        return phone

    class Config:
        orm_mode = True

#************************************************************************* JWT
class Current_User_Schema(BaseModel):
    id: int
    username: str
    email: EmailStr
    telephone: str
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "id": 12332,
                "username": "Aplaz",
                "email": "aplazidis@gmail.com",
                "telephone": "6979977872",
                "created_at": "12-2-2021, 3-Febrouario-2021"
            }
        }