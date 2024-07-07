import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app import app, db
from Model.reviews import Reviews

class ReviewsModelTestCase(unittest.TestCase):

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

    def test_reviews_creation(self):
        with app.app_context():
            review = Reviews(
                place_id='some-place-id',
                user_id='some-user-id',
                rating=5,
                comment='Test review comment'
            )
            db.session.add(review)
            db.session.commit()
            self.assertIsNotNone(review.id)
            self.assertEqual(str(review.place_id), 'some-place-id')
            self.assertEqual(str(review.user_id), 'some-user-id')
            self.assertEqual(review.rating, 5)
            self.assertEqual(review.comment, 'Test review comment')

    def test_to_dict(self):
        with app.app_context():
            review = Reviews(
                place_id='some-place-id',
                user_id='some-user-id',
                rating=5,
                comment='Test review comment'
            )
            db.session.add(review)
            db.session.commit()
            review_dict = review.to_dict()
            self.assertIn('id', review_dict)
            self.assertIn('place_id', review_dict)
            self.assertIn('user_id', review_dict)
            self.assertIn('rating', review_dict)
            self.assertIn('comment', review_dict)
            self.assertEqual(review_dict['place_id'], str(review.place_id))
            self.assertEqual(review_dict['user_id'], str(review.user_id))
            self.assertEqual(review_dict['rating'], 5)
            self.assertEqual(review_dict['comment'], 'Test review comment')

if __name__ == '__main__':
    unittest.main()

