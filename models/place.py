#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import hbnb_type_storage
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from models.amenity import Amenity
from models.review import Review


if hbnb_type_storage == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False)
                          )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if hbnb_type_storage == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', backref='place_amenities',
                                 viewonly=False, secondary=place_amenity)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def reviews(self):
        '''
        returns the list of Review instances with
        place_id equals to the current Place.id
        '''
        from models import storage
        _reviews = storage.all(Review)
        _list = []
        for r in _reviews.values():
            if r.place_id != self.id:
                continue
            _list.append(r)
        return _list

    @property
    def amenities(self):
        '''
        returns the list of Amenity instances based on the
        attribute amenity_ids that contains all Amenity.id
        linked to the Place
        '''
        from models import storage
        _amenities = storage.all(Amenity)
        _list = []
        for a in _amenities.values():
            if a.id not in self.amenity_ids:
                continue
            _list.append(amen)
        return _list

    @amenities.setter
    def amenities(self, obj):
        '''adding an Amenity.id to the attribute amenity_ids'''
        if obj is not None and isinstance(obj, Amenity):
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
