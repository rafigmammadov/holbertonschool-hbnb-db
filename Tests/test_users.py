import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.users import Users

class UsersModelTestCase(unittest.TestCase):

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

    def test_users_creation(self):
        with app.app_context():
            user = Users(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password_hash='hashed_password'
            )
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(user.id)
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.first_name, 'Test')
            self.assertEqual(user.last_name, 'User')
            self.assertEqual(user.is_admin, False)

    def test_set_password(self):
        with app.app_context():
            user = Users(
                email='test@example.com',
                first_name='Test',
                last_name='User',
            )
            user.set_password('password123')
            self.assertTrue(user.password_hash.startswith('$2b$'))

    def test_check_password(self):
        with app.app_context():
            user = Users(
                email='test@example.com',
                first_name='Test',
                last_name='User',
            )
            user.set_password('password123')
            self.assertTrue(user.check_password('password123'))
            self.assertFalse(user.check_password('wrongpassword'))

    def test_to_dict(self):
        with app.app_context():
            user = Users(
                email='test@example.com',
                first_name='Test',
                last_name='User',
            )
            db.session.add(user)
            db.session.commit()
            user_dict = user.to_dict()
            self.assertIn('id', user_dict)
            self.assertIn('email', user_dict)
            self.assertIn('first_name', user_dict)
            self.assertIn('last_name', user_dict)
            self.assertEqual(user_dict['email'], 'test@example.com')
            self.assertEqual(user_dict['first_name'], 'Test')
            self.assertEqual(user_dict['last_name'], 'User')

if __name__ == '__main__':
    unittest.main()

