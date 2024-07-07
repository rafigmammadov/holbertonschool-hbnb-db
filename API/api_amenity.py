from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from Model.amenity import Amenity
from Model.entity import db
from Persistence.data_manager import DataManager

app = Flask(__name__)
api = Api(app, version='1.0', title='Amenity API', description='A simple Amenity API')

data_manager = DataManager(db=db)

ns_amenities = Namespace('amenities', description='Amenity operations')

amenity_request_model = ns_amenities.model('AmenityRequest', {
    'name': fields.String(required=True, description='The amenity name'),
    'description': fields.String(required=True, description='The amenity description')
})

amenity_response_model = ns_amenities.model('AmenityResponse', {
    'id': fields.String(description='The amenity unique identifier'),
    'name': fields.String(description='The amenity name'),
    'description': fields.String(description='The amenity description'),
    'created_at': fields.String(description='The amenity creation timestamp'),
    'updated_at': fields.String(description='The amenity update timestamp')
})

@ns_amenities.route('/')
class AmenityList(Resource):
    @ns_amenities.doc('list_amenities')
    @ns_amenities.marshal_list_with(amenity_response_model)
    def get(self):
        amenities = []
        data = data_manager._read_data()
        if 'Amenity' in data:
            amenities = list(data['Amenity'].values())
        return amenities, 200

    @ns_amenities.doc('create_amenity')
    @ns_amenities.expect(amenity_request_model)
    @ns_amenities.marshal_with(amenity_response_model, code=201)
    def post(self):
        data = request.get_json()
        try:
            name = data['name']
            description = data['description']
            if not (name and description):
                api.abort(400, "Name and description are required.")
            
            existing_amenity = data_manager.get_by_field('name', name, 'Amenity')
            if existing_amenity:
                api.abort(409, "Amenity already exists.")

            amenity = Amenity(name=name, description=description)
            data_manager.save(amenity)
            return amenity.to_dict(), 201
        except KeyError:
            api.abort(400, "Invalid input format.")

    def new_method(self, amenity):
        return amenity.to_dict(), 201

@ns_amenities.route('/<string:amenity_id>')
@ns_amenities.response(404, 'Amenity not found')
@ns_amenities.param('amenity_id', 'The amenity identifier')
class Amenity(Resource):
    @ns_amenities.doc('get_amenity')
    @ns_amenities.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        amenity = data_manager.get(amenity_id, 'Amenity')
        if amenity:
            return amenity, 200
        else:
            api.abort(404, "Amenity not found.")

    @ns_amenities.doc('update_amenity')
    @ns_amenities.expect(amenity_request_model)
    @ns_amenities.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        data = request.get_json()
        try:
            amenity = data_manager.get(amenity_id, 'Amenity')
            if not amenity:
                api.abort(404, "Amenity not found.")
            
            updated_amenity = Amenity(
                name=data.get('name', amenity['name']),
                description=data.get('description', amenity['description'])
            )
            updated_amenity.id = amenity_id
            data_manager.update(updated_amenity)
            return updated_amenity.to_dict(), 200
        except KeyError:
            api.abort(400, "Invalid input format.")

    @ns_amenities.doc('delete_amenity')
    @ns_amenities.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        amenity = data_manager.get(amenity_id, 'Amenity')
        if not amenity:
            api.abort(404, "Amenity not found.")

        data_manager.delete(amenity_id, 'Amenity')
        return '', 204

api.add_namespace(ns_amenities)

if __name__ == '__main__':
    app.run(debug=True)
