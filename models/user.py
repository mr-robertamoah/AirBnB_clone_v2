#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from models import hbnb_type_storage
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if hbnb_type_storage == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='delete')
        reviews = relationship('Review', backref='user',
                               cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
