from flask import Flask, request
from Model.entity import db
from flask_restx import Api, Resource, fields, Namespace
from Model.place import Place
from Persistence.data_manager import DataManager
from Model.city import City
from flask_jwt_extended import jwt_required, get_jwt_identity
from Decorators.utils import admin_required

app = Flask(__name__)
api = Api(app, version='1.0', title='Place API', description='API for managing places')

data_manager = DataManager(db=db)

ns_places = Namespace('places', description='Place operations')

place_request_model = ns_places.model('PlaceRequest', {
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'address': fields.String(required=True, description='Address of the place'),
    'city_id': fields.String(required=True, description='ID of the city where the place is located'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'host_id': fields.String(required=True, description='ID of the host of the place'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms in the place'),
    'bathrooms': fields.Integer(required=True, description='Number of bathrooms in the place'),
    'price_per_night': fields.Float(required=True, description='Price per night for the place'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests the place can accommodate'),
    'amenity_ids': fields.List(fields.String, required=True, description='List of amenity IDs')
})

place_response_model = ns_places.model('PlaceResponse', {
    'id': fields.String(description='The place unique identifier'),
    'name': fields.String(description='Name of the place'),
    'description': fields.String(description='Description of the place'),
    'address': fields.String(description='Address of the place'),
    'city': fields.Nested(ns_places.model('City', {
        'id': fields.String(description='City ID'),
        'name': fields.String(description='City name'),
        'country': fields.String(description='Country code of the city'),
        'created_at': fields.String(description='City creation timestamp'),
        'updated_at': fields.String(description='City update timestamp')
    }), description='City information'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'host_id': fields.String(description='ID of the host of the place'),
    'number_of_rooms': fields.Integer(description='Number of rooms in the place'),
    'bathrooms': fields.Integer(description='Number of bathrooms in the place'),
    'price_per_night': fields.Float(description='Price per night for the place'),
    'max_guests': fields.Integer(description='Maximum number of guests the place can accommodate'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@ns_places.route('/')
class PlaceList(Resource):
    @ns_places.doc('list_places')
    @ns_places.marshal_list_with(place_response_model)
    def get(self):
        places = []
        places_data = data_manager.get_by_field('type', 'Place', 'Place')
        if places_data:
            places = [self.enrich_place_data(place) for place in places_data.values()]
        return places, 200

    @ns_places.doc('create_place')
    @ns_places.expect(place_request_model)
    @ns_places.marshal_with(place_response_model, code=201)
    @jwt_required()
    @admin_required
    def post(self):
        data = request.get_json()
        try:
            city_id = data['city_id']
            if not data_manager.get_by_field('id', city_id, 'City'):
                api.abort(404, f"City with ID '{city_id}' not found.")

            place = Place(
                name=data['name'],
                description=data['description'],
                address=data['address'],
                city_id=data['city_id'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                host_id=data['host_id'],
                number_of_rooms=data['number_of_rooms'],
                bathrooms=data['bathrooms'],
                price_per_night=data['price_per_night'],
                max_guests=data['max_guests'],
                amenities=data['amenity_ids']
            )

            data_manager.save(place)
            return self.enrich_place_data(place), 201

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_places.doc('update_place')
    @ns_places.expect(place_request_model)
    @ns_places.marshal_with(place_response_model)
    @jwt_required()
    @admin_required
    def put(self, place_id):
        data = request.get_json()
        try:
            if not data_manager.get(place_id, 'Place'):
                api.abort(404, "Place not found.")

            if not data_manager.get_by_field('id', data['city_id'], 'City'):
                api.abort(404, f"City with ID '{data['city_id']}' not found.")

            updated_place = Place(
                name=data['name'],
                description=data['description'],
                address=data['address'],
                city_id=data['city_id'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                host_id=data['host_id'],
                number_of_rooms=data['number_of_rooms'],
                bathrooms=data['bathrooms'],
                price_per_night=data['price_per_night'],
                max_guests=data['max_guests'],
                amenities=data['amenity_ids']
            )
            updated_place.id = place_id

            data_manager.update(updated_place)
            return self.enrich_place_data(updated_place), 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_places.doc('delete_place')
    @ns_places.response(204, 'Place deleted')
    @jwt_required()
    @admin_required
    def delete(self, place_id):
        if not data_manager.get(place_id, 'Place'):
            api.abort(404, "Place not found.")

        data_manager.delete(place_id, 'Place')
        return '', 204

    def enrich_place_data(self, place):
        city_data = data_manager.get(place.city_id, 'City')
        if city_data:
            city_info = {
                'id': city_data['id'],
                'name': city_data['name'],
                'country': city_data['country'],
                'created_at': city_data['created_at'],
                'updated_at': city_data['updated_at']
            }
            place_data = {
                'id': place.id,
                'name': place.name,
                'description': place.description,
                'address': place.address,
                'city': city_info,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'host_id': place.host_id,
                'number_of_rooms': place.number_of_rooms,
                'bathrooms': place.bathrooms,
                'price_per_night': place.price_per_night,
                'max_guests': place.max_guests,
                'amenities': place.amenities
            }
            return place_data
        else:
            return None


@ns_places.route('/<string:place_id>')
@ns_places.response(404, 'Place not found')
@ns_places.param('place_id', 'The place identifier')
class PlaceDetail(Resource):
    @ns_places.doc('get_place')
    @ns_places.marshal_with(place_response_model)
    def get(self, place_id):
        place = data_manager.get(place_id, 'Place')
        if place:
            return self.enrich_place_data(place), 200
        else:
            api.abort(404, "Place not found.")

    @ns_places.doc('update_place')
    @ns_places.expect(place_request_model)
    @ns_places.marshal_with(place_response_model)
    @jwt_required()
    @admin_required
    def put(self, place_id):
        data = request.get_json()
        try:
            if not data_manager.get(place_id, 'Place'):
                api.abort(404, "Place not found.")

            if not data_manager.get_by_field('id', data['city_id'], 'City'):
                api.abort(404, f"City with ID '{data['city_id']}' not found.")

            updated_place = Place(
                name=data['name'],
                description=data['description'],
                address=data['address'],
                city_id=data['city_id'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                host_id=data['host_id'],
                number_of_rooms=data['number_of_rooms'],
                bathrooms=data['bathrooms'],
                price_per_night=data['price_per_night'],
                max_guests=data['max_guests'],
                amenities=data['amenity_ids']
            )
            updated_place.id = place_id

            data_manager.update(updated_place)
            return self.enrich_place_data(updated_place), 200

        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_places.doc('delete_place')
    @ns_places.response(204, 'Place deleted')
    @jwt_required()
    @admin_required
    def delete(self, place_id):
        if not data_manager.get(place_id, 'Place'):
            api.abort(404, "Place not found.")

        data_manager.delete(place_id, 'Place')
        return '', 204

    def enrich_place_data(self, place):
        city_data = data_manager.get(place.city_id, 'City')
        if city_data:
            city_info = {
                'id': city_data['id'],
                'name': city_data['name'],
                'country': city_data['country'],
                'created_at': city_data['created_at'],
                'updated_at': city_data['updated_at']
            }
            place_data = {
                'id': place.id,
                'name': place.name,
                'description': place.description,
                'address': place.address,
                'city': city_info,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'host_id': place.host_id,
                'number_of_rooms': place.number_of_rooms,
                'bathrooms': place.bathrooms,
                'price_per_night': place.price_per_night,
                'max_guests': place.max_guests,
                'amenities': place.amenities
            }
            return place_data
        else:
            return None
