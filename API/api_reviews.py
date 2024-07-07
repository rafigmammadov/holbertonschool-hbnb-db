from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace
from Model.reviews import Reviews
from flask_jwt_extended import jwt_required
from Model.entity import db
from Persistence.data_manager import DataManager
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Review API', description='API for managing reviews')

ns_reviews = Namespace('reviews', description='Review operations')

data_manager = DataManager(db=db)

review_request_model = ns_reviews.model('ReviewRequest', {
    'user_id': fields.String(required=True, description='ID of the user writing the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='Comment about the place')
})

review_response_model = ns_reviews.model('ReviewResponse', {
    'id': fields.String(description='The review unique identifier'),
    'place_id': fields.String(description='ID of the place'),
    'user_id': fields.String(description='ID of the user writing the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'comment': fields.String(description='Comment about the place'),
    'created_at': fields.String(description='Review creation timestamp'),
    'updated_at': fields.String(description='Review update timestamp')
})

@ns_reviews.route('/places/<string:place_id>/reviews')
class PlaceReviews(Resource):
    @ns_reviews.doc('create_place_review')
    @ns_reviews.expect(review_request_model)
    @ns_reviews.marshal_with(review_response_model, code=201)
    @jwt_required()
    def post(self, place_id):
        data = request.get_json()
        try:
            user_id = data['user_id']
            rating = data['rating']
            comment = data['comment']

            if not (1 <= rating <= 5):
                api.abort(400, "Rating should be between 1 and 5.")

            if not data_manager.get(user_id, 'Users'):
                api.abort(404, f"User with ID '{user_id}' not found.")
            
            if not data_manager.get(place_id, 'Place'):
                api.abort(404, f"Place with ID '{place_id}' not found.")

            review = Reviews(place_id, user_id, rating, comment)
            data_manager.save(review)

            return review.to_dict(), 201

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_reviews.doc('get_place_reviews')
    @ns_reviews.marshal_list_with(review_response_model)
    def get(self, place_id):
        reviews = []
        reviews_data = data_manager.get_by_field('place_id', place_id, 'Reviews')
        if reviews_data:
            reviews = [review for review in reviews_data.values()]
        return reviews, 200

@ns_reviews.route('/users/<string:user_id>/reviews')
class UserReviews(Resource):
    @ns_reviews.doc('get_user_reviews')
    @ns_reviews.marshal_list_with(review_response_model)
    def get(self, user_id):
        reviews = []
        reviews_data = data_manager.get_by_field('user_id', user_id, 'Reviews')
        if reviews_data:
            reviews = [review for review in reviews_data]
        return reviews, 200

@ns_reviews.route('/reviews/<string:review_id>')
@ns_reviews.response(404, 'Review not found')
@ns_reviews.param('review_id', 'The review identifier')
class Review(Resource):
    @ns_reviews.doc('get_review')
    @ns_reviews.marshal_with(review_response_model)
    def get(self, review_id):
        review = data_manager.get(review_id, 'Reviews')
        if review:
            return review, 200
        else:
            api.abort(404, "Review not found.")

    @ns_reviews.doc('update_review')
    @ns_reviews.expect(review_request_model)
    @ns_reviews.marshal_with(review_response_model)
    @jwt_required()
    def put(self, review_id):
        data = request.get_json()
        try:
            review = data_manager.get(review_id, 'Reviews')
            if not review:
                api.abort(404, "Review not found.")
            
            review.update({
                'rating': data.get('rating', review['rating']),
                'comment': data.get('comment', review['comment']),
                'updated_at': datetime.now().isoformat()
            })

            data_manager.update(review)
            return review, 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_reviews.doc('delete_review')
    @ns_reviews.response(204, 'Review deleted')
    @jwt_required()
    def delete(self, review_id):
        review = data_manager.get(review_id, 'Reviews')
        if not review:
            api.abort(404, "Review not found.")

        data_manager.delete(review_id, 'Reviews')
        return '', 204

api.add_namespace(ns_reviews)

if __name__ == '__main__':
    app.run(debug=True)
