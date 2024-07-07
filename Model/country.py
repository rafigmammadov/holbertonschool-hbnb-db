#!/usr/bin/python3
"""
Module that contains Country Model
"""
import json
from .entity import EntityMixin, db
from sqlalchemy.orm import relationship

class Country(db.Model, EntityMixin):
    __tablename__ = 'countries'

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cities = relationship('City', backref='country', lazy=True)

    def __init__(self, code, name):

        self.code = code
        self.name = name
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def __repr__(self):
        return (f"Country(id={self.id}, code='{self.code}', name='{self.name}', cities={self.cities})")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'code': self.code,
            'name': self.name,
            'cities': [city.to_dict() for city in self.cities]
        })
        return data
