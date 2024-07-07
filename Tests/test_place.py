import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.place import Place

class PlaceModelTestCase(unittest.TestCase):

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

    def test_place_creation(self):
        with app.app_context():
            place = Place(
                name='Test Place',
                description='Test Description',
                address='123 Test St',
                city_id='some-city-id',
                latitude=40.7128,
                longitude=-74.0060,
                host_id='some-host-id',
                number_of_rooms=2,
                bathrooms=1,
                price_per_night=100.0,
                max_guests=4,
                amenities='WiFi, Parking'
            )
            db.session.add(place)
            db.session.commit()
            self.assertIsNotNone(place.id)
            self.assertEqual(place.name, 'Test Place')
            self.assertEqual(place.description, 'Test Description')
            self.assertEqual(place.address, '123 Test St')
            self.assertEqual(str(place.city_id), 'some-city-id')
            self.assertEqual(place.latitude, 40.7128)
            self.assertEqual(place.longitude, -74.0060)
            self.assertEqual(str(place.host_id), 'some-host-id')
            self.assertEqual(place.number_of_rooms, 2)
            self.assertEqual(place.bathrooms, 1)
            self.assertEqual(place.price_per_night, 100.0)
            self.assertEqual(place.max_guests, 4)
            self.assertEqual(place.amenities, 'WiFi, Parking')

    def test_to_dict(self):
        with app.app_context():
            place = Place(
                name='Test Place',
                description='Test Description',
                address='123 Test St',
                city_id='some-city-id',
                latitude=40.7128,
                longitude=-74.0060,
                host_id='some-host-id',
                number_of_rooms=2,
                bathrooms=1,
                price_per_night=100.0,
                max_guests=4,
                amenities='WiFi, Parking'
            )
            db.session.add(place)
            db.session.commit()
            place_dict = place.to_dict()
            self.assertIn('id', place_dict)
            self.assertIn('name', place_dict)
            self.assertIn('description', place_dict)
            self.assertIn('address', place_dict)
            self.assertIn('city_id', place_dict)
            self.assertIn('latitude', place_dict)
            self.assertIn('longitude', place_dict)
            self.assertIn('host_id', place_dict)
            self.assertIn('number_of_rooms', place_dict)
            self.assertIn('bathrooms', place_dict)
            self.assertIn('price_per_night', place_dict)
            self.assertIn('max_guests', place_dict)
            self.assertIn('amenities', place_dict)
            self.assertEqual(place_dict['name'], 'Test Place')
            self.assertEqual(place_dict['description'], 'Test Description')
            self.assertEqual(place_dict['address'], '123 Test St')
            self.assertEqual(place_dict['city_id'], str(place.city_id))
            self.assertEqual(place_dict['latitude'], 40.7128)
            self.assertEqual(place_dict['longitude'], -74.0060)
            self.assertEqual(place_dict['host_id'], str(place.host_id))
            self.assertEqual(place_dict['number_of_rooms'], 2)
            self.assertEqual(place_dict['bathrooms'], 1)
            self.assertEqual(place_dict['price_per_night'], 100.0)
            self.assertEqual(place_dict['max_guests'], 4)
            self.assertEqual(place_dict['amenities'], 'WiFi, Parking')

if __name__ == '__main__':
    unittest.main()

