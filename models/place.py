#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from models.user import User
from models.city import City
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
import os
from sqlalchemy import Table, Column, Integer, ForeignKey


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
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
    amenity_ids = []

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship("Review", backref="place",
                               cascade="delete")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            rev_list = []
            for obj in models.storage.all(Review):
                if obj.place_id == self.id:
                    rev_list.append(obj)

        @amenities.setter
        def amenities(self, obj=None):
            if not obj is None and type(obj) is Amenity:
                self.amenity_ids.append(obj.id)

        @property
        def amenities(self):
            ins_list = []
            for obj in models.storage.all(Amenity):
                if obj.id in self.amenity_ids:
                    ins_list.append(obj)
            return ins_list
