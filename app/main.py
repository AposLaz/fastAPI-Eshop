from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.param_functions import Body

from app.routers import items
from app.routers import users
from app.routers import auth 
from app.routers import votes

from app.db import models
from app.db.db import engine

from fastapi.middleware.cors import CORSMiddleware
#------------------------------------------------------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# exception handler for authjwt
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    if str(exc.message) == "Signature has expired":

        # An o xronos gia to TOken elixe tote kalese ti refresh gia neo token
        # An o xronos einai sta 30 second diafora kalese ti refresh gia neo token

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Oh sig expired :D"}
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

# **** Routers
app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"msg":"Hello World"}