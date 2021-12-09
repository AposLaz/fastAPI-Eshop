#*************************
#    HASHING PASSWORD    *
#*************************

from passlib.context import CryptContext

#deprecated = refers to functions or elements that are in the process of being replaced by newer ones
#Set method for hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_hash_pwd(pwd):
    hashed_pwd = pwd_context.hash(pwd)
    return hashed_pwd

# Verify if password that user gave is the same with hash password in database
def verify_user(pwd,hash_pwd):
    return pwd_context.verify(pwd,hash_pwd)
     
