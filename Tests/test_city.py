import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.city import City

class CityModelTestCase(unittest.TestCase):

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

    def test_city_creation(self):
        with app.app_context():
            city = City(country='Test Country', name='Test City')
            db.session.add(city)
            db.session.commit()
            self.assertIsNotNone(city.id)
            self.assertEqual(city.country, 'Test Country')
            self.assertEqual(city.name, 'Test City')

    def test_city_to_dict(self):
        with app.app_context():
            city = City(country='Test Country', name='Test City')
            db.session.add(city)
            db.session.commit()
            city_dict = city.to_dict()
            self.assertEqual(city_dict['country'], 'Test Country')
            self.assertEqual(city_dict['name'], 'Test City')

if __name__ == '__main__':
    unittest.main()

