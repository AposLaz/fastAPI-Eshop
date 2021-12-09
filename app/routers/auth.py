#******************************************
#*       Here we authenticate Users       *
#******************************************


from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi_jwt_auth.auth_jwt import AuthJWT
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from app.schema.v1.token import Token_Schema
from app.routers import user_routines, hash_pwd, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

import datetime

from app.db.db import get_db

from app.configs.config import environment

router = APIRouter(
    tags=["Authentication"]
)

class Auth_Settings_Token(BaseModel):
    authjwt_algorithm: str = environment.algorithm
    authjwt_secret_key: str = environment.secret_key
    authjwt_access_token_expires: int = environment.access_token_expire_seconds #seconds
    authjwt_refresh_token_expires : int = environment.refresh_token_expire_seconds


@AuthJWT.load_config
def get_config():
    return Auth_Settings_Token()


@router.post('/login', response_model=Token_Schema)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # First check if user exists
    user = user_routines.get_user_by_username(user_credentials,db) 
    
    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail={"Error":"User does not exists"})
    
    # If user exists check if password is valid
    if not hash_pwd.verify_user(user_credentials.password, user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail={"Error":"Invalid Credentials"})

    # return token
    tokens = oauth2.create_jwt_token(user.id, Authorize)
    return tokens

#**************** Logout

#---------------- Logout end here

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.get('/test')
def test(Authorize: AuthJWT = Depends()):
    exp_jwt = oauth2.expire_jwt(Authorize) * 1000
    milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000
    if milliseconds_since_epoch >= exp_jwt:
        return "Token expired"
    return "Token valiable"