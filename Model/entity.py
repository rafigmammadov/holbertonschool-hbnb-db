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
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# entity_mixin.py
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EntityMixin:
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        self.id = uuid.uuid4()
        gmt4_offset = timedelta(hours=-4)
        gmt4 = timezone(gmt4_offset)
        now = datetime.now(gmt4)
        self.created_at = now
        self.updated_at = now

    def to_dict(self):
        """
        Converts the EntityMixin instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the entity's data.
        """
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Entity(db.Model, EntityMixin):
    __tablename__ = 'entities'

    def __init__(self):
        super().__init__()
