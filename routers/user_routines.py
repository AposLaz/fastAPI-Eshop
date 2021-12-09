#**************************************************
#*   All functions that called from user routers  *
#**************************************************


from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND
from db.models import Users_Model
from schema.v1.users import Users_Schema

from .hash_pwd import get_hash_pwd

def get_all_users(db: Session, search):
    users = db.query(Users_Model).filter(Users_Model.username.contains(search)).all()
    return users

def get_user_by_id(id: int, db: Session):
    user = db.query(Users_Model).filter(Users_Model.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail={"Error":"User does not exist"})

def get_user_by_username(user_cred, db: Session):
    user_pwd = db.query(Users_Model).filter(Users_Model.username == user_cred.username).first()
    return user_pwd

def create_user(user: Users_Schema, db: Session):
    user.password = get_hash_pwd(user.password)                         # hash password
    users = Users_Model(**user.dict())                                  # its database model not schema
    db.add(users)
    db.commit()   
    #db.refresh(users)
    return 

def find_user_db(user_id, db: Session):
    user = db.query(Users_Model).filter(Users_Model.id == user_id)
    if user.first():
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error ": "User not found"})

def update_users_byID(user_id, payload: dict, db: Session):
    find_user = find_user_db(user_id, db)
    find_user.update(payload,synchronize_session=False)
    db.commit()
    # db.refresh(user)
    return

def delete_users_byID(user_id,db: Session):
    find_user = find_user_db(user_id,db)
    find_user.delete(synchronize_session=False)
    db.commit()
    return 