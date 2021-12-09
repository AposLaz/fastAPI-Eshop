from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from configs.config import environment

def create_db():
    try:
        SQLALCHEMY_DATABASE_URL = f'postgresql://{environment.database_username}:{environment.database_password}@{environment.database_hostname}:{environment.database_port}/{environment.database_name}'

        engine = create_engine(SQLALCHEMY_DATABASE_URL)

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        Base = declarative_base()
        
        print("Connected to Database")

        database_dep = [Base,engine,SessionLocal]
        return database_dep
        
    except Exception as e:
        print("Could not connect in database")
        print("Error : ",e)

### RETURN FROM DATABASE
database_dep = create_db()

# VALUES THAT NEED IN OTHER FILES
Base = database_dep[0]
engine = database_dep[1]
SessionLocal = database_dep[2]


#******** Dependency for DATABASE *******
# DEPENDS FOR CLOSE SESSION WITH DB AFTER CALL
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




