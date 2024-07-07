#!/usr/bin/python3
"""
Module that contains Place Model
"""
from .entity import db, EntityMixin
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

place_amenity_association = db.Table('place_amenity_association',
    db.Column('place_id', UUID(as_uuid=True), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', UUID(as_uuid=True), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(db.Model, EntityMixin):
    __tablename__ = 'places'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=False)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cities.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    amenities = db.relationship('Amenity', secondary=place_amenity_association, lazy='subquery',
                                backref=db.backref('places', lazy=True))
    
    def __init__(self, name, description, address, city_id, latitude,
                 longitude, host_id, number_of_rooms, bathrooms,
                 price_per_night, max_guests, amenities):
        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities

    def __repr__(self):
        return (f"Place(id={self.id}, name='{self.name}'"
                f"description='{self.description}', "
                f"address='{self.address}', city_id={self.city_id}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, host_id={self.host_id}, "
                f"number_of_rooms={self.number_of_rooms}, "
                f"bathrooms={self.bathrooms}, "
                f"price_per_night={self.price_per_night}, "
                f"max_guests={self.max_guests}, "
                f"amenities={self.amenities})")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': str(self.city_id),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': str(self.host_id),
            'number_of_rooms': self.number_of_rooms,
            'bathrooms': self.bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': self.amenities
        })
        return data
