from typing import Optional
from fastapi import APIRouter, Depends,Response
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from sqlalchemy.sql.elements import Null
from starlette import status
from routers import oauth2
from fastapi_jwt_auth import AuthJWT

# schema
from schema.v1.users import Users_Schema, Current_User_Schema, Update_User_Schema

# db
from db.db import get_db
from sqlalchemy.orm import Session

#routines
from routers import user_routines 

router = APIRouter(prefix="/users",
                   tags=["users"])

#************************************* GET

@router.get("/", status_code= status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), 
              current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user),
              search: Optional[str] = ""): 
    try:
        get_users = user_routines.get_all_users(db,search)                 #query parameter search means that i can filter users by name
                                                                    #does not require ''exact'' match
        return get_users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= {"Error ":"Internal Server Error"})


@router.get("/{user_id}",status_code=status.HTTP_200_OK)
def get_user_id(user_id: int, db: Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    user = user_routines.get_user_by_id(user_id, db)
    return user

#------------------------------ GET END HERE

#******************************* POST USER

#********* user_id: int = Depends(oauth2.get_current_user) -> User must log in before create a new user

@router.post("/")
def create_users(user: Users_Schema, db: Session = Depends(get_db)):
    try:
        post_user = user_routines.create_user(user,db)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=e)
    

#---------------------------- POST END HERE

#*************** Update user

@router.patch('/{user_id}')
def update_user(user_id, payload: Update_User_Schema, db: Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    payload = payload.dict()
    payload = {key: value for (key,value) in payload.items() if value }             # get only key:value pair if values != None
    update = user_routines.update_users_byID(user_id, payload, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#---------------- Update end here


#*************** Delete user

@router.delete('/{user_id}')
def delete_user(user_id, db:Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    delete = user_routines.delete_users_byID(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#---------------- Delete end here

