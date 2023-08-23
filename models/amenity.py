#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import hbnb_type_storage
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """ Representation of amenities """
    __tablename__ = 'amenities'
    if hbnb_type_storage == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
