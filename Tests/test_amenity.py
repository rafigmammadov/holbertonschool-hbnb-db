#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.amenity import Amenity

class TestAmenity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_amenity(self):

        amenity = Amenity(name='WiFi', description='Wireless internet connection')

        with app.app_context():
            db.session.add(amenity)
            db.session.commit()


        self.assertIsNotNone(amenity.id)

    def test_to_dict(self):

        amenity = Amenity(name='Pool', description='Private swimming pool')

        with app.app_context():
            db.session.add(amenity)
            db.session.commit()


        amenity_dict = amenity.to_dict()


        self.assertIn('id', amenity_dict)
        self.assertEqual(amenity_dict['name'], 'Pool')
        self.assertEqual(amenity_dict['description'], 'Private swimming pool')

if __name__ == '__main__':
    unittest.main()


