import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from datetime import datetime, timedelta
from app import app, db
from Model.entity import Entity

class EntityModelTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_entity_creation(self):
        with app.app_context():
            entity = Entity()
            db.session.add(entity)
            db.session.commit()
            self.assertIsNotNone(entity.id)
            self.assertIsInstance(entity.created_at, datetime)
            self.assertIsInstance(entity.updated_at, datetime)

    def test_to_dict(self):
        with app.app_context():
            entity = Entity()
            db.session.add(entity)
            db.session.commit()
            entity_dict = entity.to_dict()
            self.assertIn('created_at', entity_dict)
            self.assertIn('updated_at', entity_dict)
            self.assertEqual(entity_dict['created_at'], entity.created_at.isoformat())
            self.assertEqual(entity_dict['updated_at'], entity.updated_at.isoformat())

    def test_update_timestamps(self):
        with app.app_context():
            entity = Entity()
            db.session.add(entity)
            db.session.commit()

            original_created_at = entity.created_at
            original_updated_at = entity.updated_at

            # Simulate an update after a delay
            entity.some_attribute = 'updated value'
            db.session.commit()

            self.assertEqual(entity.created_at, original_created_at)
            self.assertGreater(entity.updated_at, original_updated_at)

if __name__ == '__main__':
    unittest.main()

