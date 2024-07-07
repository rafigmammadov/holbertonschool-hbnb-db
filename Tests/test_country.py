import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.country import Country
from Model.city import City

class CountryModelTestCase(unittest.TestCase):

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

    def test_country_creation(self):
        with app.app_context():
            country = Country(country_code='US', name='United States')
            db.session.add(country)
            db.session.commit()
            self.assertIsNotNone(country.id)
            self.assertEqual(country.country_code, 'US')
            self.assertEqual(country.name, 'United States')

    def test_country_to_dict(self):
        with app.app_context():
            country = Country(country_code='US', name='United States')
            db.session.add(country)

            city1 = City(country='US', name='New York')
            city2 = City(country='US', name='Los Angeles')

            country.add_city(city1)
            country.add_city(city2)

            db.session.add(city1)
            db.session.add(city2)
            db.session.commit()

            country_dict = country.to_dict()
            self.assertEqual(country_dict['country_code'], 'US')
            self.assertEqual(country_dict['name'], 'United States')
            self.assertEqual(len(country_dict['cities']), 2)
            self.assertEqual(country_dict['cities'][0]['name'], 'New York')
            self.assertEqual(country_dict['cities'][1]['name'], 'Los Angeles')

    def test_invalid_country_code(self):
        with app.app_context():
            with self.assertRaises(ValueError):
                country = Country(country_code='XYZ', name='Invalid Country')
                db.session.add(country)
                db.session.commit()

if __name__ == '__main__':
    unittest.main()

