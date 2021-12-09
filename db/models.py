#***************************
#*     CREATE DATABASE     *
#***************************

from sqlalchemy import Column, String, Integer, Float, Boolean, ARRAY
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .db import Base
from sqlalchemy.orm import Session

class Items_Model(Base):

    __tablename__="items"

    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String,nullable=False)
    type = Column(String,nullable=False)
    description = Column(String,nullable=False)
    tags = Column(ARRAY(String),nullable=False)
    price = Column(Float,nullable=False)
    available = Column(Boolean,nullable=False)
    inventory = Column(Integer,nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE"), nullable=False)

class Users_Model(Base):

    __tablename__ ="users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telephone = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Votes_Model(Base):

    __tablename__ = "votes"

    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)