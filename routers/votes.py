from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from starlette import status
from starlette.responses import Response

from schema.v1.users import Current_User_Schema
from schema.v1.votes import Votes_Schema

from db.db import get_db
from db.models import Items_Model, Votes_Model

from fastapi_jwt_auth import AuthJWT
from routers import oauth2

from routers import item_routines

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)

def vote_item(item_id,user_id, like, db: Session):
    exists_vote = db.query(Votes_Model).filter(Votes_Model.item_id == item_id, Votes_Model.user_id == user_id)        # check if like exists from this user
    if like == 1 :                                  
        if exists_vote.first():                                                    
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Error":"You can do only one like"})
        
        new_vote = Votes_Model(item_id = item_id, user_id = user_id)
        db.add(new_vote)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        if not exists_vote.first():                                                    
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error":"Like do not found"}) # do not send anything

        exists_vote.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_200_OK)



@router.post("/")
def post_vote(vote: Votes_Schema, db: Session = Depends(get_db) , current_user: Current_User_Schema= Depends(oauth2.verify_jwt_token_get_current_user)):
    tmp = vote_item(vote.item_id, current_user.id, vote.like, db)
    return tmp