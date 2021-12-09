from pydantic import BaseSettings

class Environment(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str 
    database_name : str
    database_username: str
    secret_key : str
    algorithm : str
    access_token_expire_seconds : int
    refresh_token_expire_seconds : int 

    #import from .env file
    class Config:
        env_file = ".env"

environment = Environment()