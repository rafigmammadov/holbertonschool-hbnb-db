#!/usr/bin/python3
"""
Module that contains Country Model
"""
import json
from .entity import Entity, db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

def load_iso_3166_1_data(filepath='countries.json'):
    with open(filepath, 'r') as file:
        return json.load(file)

iso_3166_1_data = load_iso_3166_1_data()

class Country(Entity):
    __tablename__ = 'countries'

    _country_code = db.Column('country_code', db.String(2), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    cities = relationship('City', backref='country', lazy=True)

    @hybrid_property
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, value):
        if value not in iso_3166_1_data:
            raise ValueError(f"Invalid country code: {value}")
        self._country_code = value

    def add_city(self, city):
        self.cities.append(city)

    def __repr__(self):
        return (f"Country(id={self.id}, country_code='{self.country_code}', name='{self.name}', cities={self.cities})")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'country_code': self.country_code,
            'name': self.name,
            'cities': [city.to_dict() for city in self.cities]
        })
        return data
