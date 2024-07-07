import os
import json
from uuid import UUID
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class DataManager:
    def __init__(self, db=None, filename="database.json", use_database=False):
        self.filename = filename
        self.use_database = use_database
        self.db = db

        if not self.use_database and not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)

    def _read_data(self):
        if self.use_database:
            return None

        try:
            with open(self.filename, 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def _write_data(self, data):
        if self.use_database:
            return

        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, cls=UUIDEncoder)

    def save(self, entity):
        if self.use_database:
            try:
                self.db.session.add(entity)
                self.db.session.commit()
            except IntegrityError:
                self.db.session.rollback()
                raise
        else:
            data = self._read_data()
            entity_type = type(entity).__name__
            entity_id = str(getattr(entity, 'id', None))

            if entity_type not in data:
                data[entity_type] = {}

            data[entity_type][entity_id] = entity.__dict__
            self._write_data(data)

    def get(self, entity_id, entity_type):
        if self.use_database:
            model = globals()[entity_type]
            return self.db.session.query(model).get(entity_id)

        data = self._read_data()
        entity_id = str(entity_id)
        if entity_type in data and entity_id in data[entity_type]:
            return data[entity_type][entity_id]

        return None

    def update(self, entity):
        if self.use_database:
            try:
                self.db.session.commit()
            except IntegrityError:
                self.db.session.rollback()
                raise
        else:
            data = self._read_data()
            entity_type = type(entity).__name__
            entity_id = str(getattr(entity, 'id', None))

            if entity_type in data and entity_id in data[entity_type]:
                data[entity_type][entity_id] = entity.__dict__
                self._write_data(data)
            else:
                raise ValueError(f"Entity of type {entity_type} "
                                 f"with id {entity_id} not found")

    def delete(self, entity_id, entity_type):
        if self.use_database:
            model = globals()[entity_type]
            entity = self.db.session.query(model).get(entity_id)
            if entity:
                self.db.session.delete(entity)
                self.db.session.commit()
            else:
                raise ValueError(f"Entity of type {entity_type} "
                                 f"with id {entity_id} not found")
        else:
            data = self._read_data()
            entity_id = str(entity_id)

            if entity_type in data and entity_id in data[entity_type]:
                del data[entity_type][entity_id]

                if not data[entity_type]:
                    del data[entity_type]
                self._write_data(data)
            else:
                raise ValueError(f"Entity of type {entity_type} "
                                 f"with id {entity_id} not found")
    
    def get_by_field(self, field, value, entity_type):
        if self.use_database:
            model = globals()[entity_type]
            return self.db.session.query(model).filter(getattr(model, field) == value).first()

        data = self._read_data()
        if entity_type in data:
            for entity_id, entity in data[entity_type].items():
                if entity.get(field) == value:
                    return entity
        return None
