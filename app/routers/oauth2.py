#********************************
#           JWT TOKENS          *
#********************************

#--- https://indominusbyte.github.io/fastapi-jwt-auth/api-doc/

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm.session import Session
from app.db.models import Users_Model
from app.db.db import get_db
from app.schema.v1.token import Token_Data_Schema
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

#*****************
#*     STEPS     *
#*****************

# 1) -> SECRET KEY
# 2) -> Algorithm
# 3) -> Expiration Time
# 4) -> Payload = (data, expiration time)
# 5) -> JWT_token = (Payload, SECRET KEY, Algorithm)



def create_jwt_token(data, Authorize: AuthJWT):
    access_token = Authorize.create_access_token(subject=data)
    refresh_token = Authorize.create_refresh_token(subject=data)
    tokens = {
         "access_token": access_token,
         "refresh_token": refresh_token
        }
    return tokens

#****** VERIFY JWT TOKEN
# Decode the received token, verify it, and return the current user.
# credentials_exception = if have issues with token orcredentials do not match

def verify_jwt_token_get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    current_user = db.query(Users_Model).filter(Users_Model.id == user_id).first()
    return current_user


def expire_jwt(Authorize: AuthJWT):
    Authorize.jwt_required()
    expiration_time = Authorize.get_raw_jwt()["exp"]
    return expiration_time


## In our endpoint, we will only get a user if the user exists, was correctly authenticated, and is active

# Pass this function as a dependency ** in every router **
# So anytime that we have a specific endpoint that should be protected and that means that user 
# should be logged in to use it, we USE in ROUTERS 
# function -> get_current_user

# This function : 
# 1) take the Token from the Request automatically
# 2) Extract the id for us
# 3) Verify that Token is correct with function ** verify_jwt_token() **
# 4) Exctract the << ID >>, fetch the user from database and then add << ID >> as a parameter in routers 
#
#
# IF NO ERROR then USER has a Valid Token and RETURN users ***<<<< ID >>>>*****
