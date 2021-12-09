#**************************************************
#*   All functions that called from items routers  *
#**************************************************

from fastapi.exceptions import HTTPException
from sqlalchemy.sql.functions import func
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.schema.v1.items import Create_Items_Schema
from app.db.models import Items_Model, Votes_Model
from sqlalchemy.orm import Session

def get_all_items(db: Session, search):
    items = db.query(Items_Model, func.count(Votes_Model.item_id).label("likes")).join(
        Votes_Model,Items_Model.id == Votes_Model.item_id, isouter = True).group_by(Items_Model.id).filter(
            Items_Model.type.contains(search)).all()
    return items



def get_items_by_name(name: str ,db:Session):
    items = db.query(Items_Model, func.count(Items_Model.id).label("likes")).join(
        Votes_Model, Votes_Model.item_id == Items_Model.id, isouter = True).group_by(Items_Model.id).filter(Items_Model.name == name).first()
    return items



def get_item_by_id(item_id: int, db: Session):
    items = db.query(Items_Model).filter(Items_Model.id == item_id)
    if items == None:
        return False
    return items


def create_items(currend_user_id,product: Create_Items_Schema, db: Session):
        item = Items_Model(owner_id=currend_user_id,**product.dict())
        db.add(item)
        db.commit()
        #db.refresh(item)
        return  



def update_by_id(item_id,payload,db: Session, user_id):
    find_item = get_item_by_id(item_id,db)
    if find_item.first():                                               #find item with this id
        if find_item.first().owner_id == user_id:                       #check if y are the owner
            find_item.update(payload,synchronize_session=False)
            db.commit()
            return None
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail = {"Error":"Not authorized to perform this action"})
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f'Product did not found') 



def delete_by_id(item_id: int,db: Session, user_id):
    find_item = get_item_by_id(item_id,db) 
    if find_item.first():                                               #find item with this id
        if find_item.first().owner_id == user_id:                       #check if y are the owner
            find_item.delete(synchronize_session=False)
            db.commit()
            return None
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail = {"Error":"Not authorized to perform this action"})
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f'Product did not found')



