#!/usr/bin/python3
"""
Module that contains Country Model
"""
import json
from .entity import EntityMixin, db

class Country(db.Model, EntityMixin):
    __tablename__ = 'countries'

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, code, name):

        self.code = code
        self.name = name

    def add_city(self, city):
        self.cities.append(city)

    def __repr__(self):
        return (f"Country(id={self.id}, code='{self.code}', name='{self.name}')")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'code': self.code,
            'name': self.name,
        })
        return data
