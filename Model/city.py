#!/usr/bin/python3
"""
Module that contains City Model
"""
from .entity import EntityMixin, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

class City(db.Model, EntityMixin):
    __tablename__ = 'cities'

    country = db.Column(db.String, db.ForeignKey('countries.code'), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, country, name):
        super().__init__()
        self.country = country
        self.name = name

    def __repr__(self):
        return (f"City(country={self.country}, name='{self.name}')")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'id': self.id,
            'country': self.country,
            'name': self.name
        })
        return data
