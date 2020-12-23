# pylint: disable=no-name-in-module

from typing import Optional

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String


Base = declarative_base()


class Sample(BaseModel):
    id: int
    user_id: int
    card_id: int
    state: str
    wts: bool

class SampleNew(BaseModel):
    user_id: int
    card_id: int
    state: str
    wts: bool

class SampleUpdate(BaseModel):
    user_id: Optional[int] = None
    card_id: Optional[int] = None
    state: Optional[str] = None
    wts: Optional[bool] = None

class NewSampleID(BaseModel):
    id: int


class Wish(BaseModel):
    id: int
    user_id: int
    card_id: int

class WishNew(BaseModel):
    user_id: int
    card_id: int

class WishUpdate(BaseModel):
    user_id: Optional[int]
    card_id: Optional[int]

class NewWishID(BaseModel):
    id: int


class SampleModel(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, index = True)
    card_id = Column(Integer, index = True)
    state = Column(String)
    wts = Column(Boolean, index = True)

class WishModel(Base):
    __tablename__ = "wishes"
    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, index = True)
    card_id = Column(Integer, index = True)
