#!/usr/bin/python3
"""
Module that contains City Model
"""
from .entity import Entity, db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class City(Entity):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

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
