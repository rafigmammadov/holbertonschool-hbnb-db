#!/usr/bin/python3
"""
Base class for all entities in the application. This class provides
    common attributes and methods that are shared across different models.

    Attributes:
        id (UUID): A unique identifier for the entity, generated using UUID4 to ensure global uniqueness.
        created_at (datetime): The timestamp when the entity was created.
        updated_at (datetime): The timestamp when the entity was last updated.
"""
import uuid
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entity(db.Model):
    __tablename__ = 'entities'
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    updated_at = db.Column(db.DateTime, nullable=False,
                        default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Converts the Entity instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the entity's data.
        """
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
