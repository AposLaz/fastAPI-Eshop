# create, retrieve, update, delete items

from typing import Optional
from fastapi import APIRouter,status, Depends, Response, HTTPException
from fastapi.param_functions import Body
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

# schema
from app.schema.v1.items import Create_Items_Schema
from app.schema.v1.users import Current_User_Schema

# db
from sqlalchemy.orm import Session
from app.db.db import get_db

# routines 
from app.routers import item_routines

# JWT
from app.routers import oauth2

#*********************************
#    5:38:57 Response Model -> FRO DO NOT RETURN --> ID <-- IN RESPONSE
#
#      RELATIONSHIPS TOO IMPORTANT
#
#*********************************

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/",status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user),
            search: Optional[str] = "" ):
    try:
        items = item_routines.get_all_items(db, search)
        return items
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail= {"Error ":"Internal Server Error"})




@router.get("/{item_id}",status_code=status.HTTP_200_OK)
def get_one(item_id: str, db: Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    items = item_routines.get_items_by_name(item_id,db)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"The products does not exist")
    return items
    




@router.post("/")
def create_items(food: Create_Items_Schema, db: Session = Depends(get_db), current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    try:
        post_food = item_routines.create_items(current_user.id,food,db)
        return Response(status_code=HTTP_201_CREATED) 
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail= {"Error ":"Internal Server Error"})




@router.put("/{item_id}")
def update_items(item_id, payload= Body(...), db: Session = Depends(get_db),current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    update_item = item_routines.update_by_id(item_id,payload,db, current_user.id)
    return Response(status_code=HTTP_204_NO_CONTENT)




@router.delete("/{item_id}")
def delete_items(item_id, db: Session = Depends(get_db),current_user: Current_User_Schema = Depends(oauth2.verify_jwt_token_get_current_user)):
    delete_item = item_routines.delete_by_id(item_id,db, current_user.id)
    return Response(status_code=HTTP_204_NO_CONTENT)

