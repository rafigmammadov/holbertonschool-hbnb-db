#!/usr/bin/python3
"""
Module that contains Users Model
"""
from .entity import Entity, db
from sqlalchemy.dialects.postgresql import UUID
from flask_bcrypt import Bcrypt
import uuid
from app import app

bcrypt = Bcrypt(app)

class Users(Entity):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
         return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return (f"Users(id={self.id}, email='{self.email}', "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}')")

    def to_dict(self):
        """
        Converts the Users instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the user's data.
        """
        data = super().to_dict()
        data.update({
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        return data
