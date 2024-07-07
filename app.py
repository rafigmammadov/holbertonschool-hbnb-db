#!/usr/bin/python3
import os
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from Model.entity import db
from create_admin import create_admin_user
from API.api_users import ns_users
from API.api_country_city import ns_city, ns_country
from API.api_places import ns_places
from API.api_reviews import ns_reviews
from API.api_amenity import ns_amenities

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable to suppress warning

app.config['JWT_SECRET_KEY'] = 'aminarufatrafig'
jwt = JWTManager(app)

# Initialize SQLAlchemy instance
db.init_app(app)

# Create the development database if it doesn't exist
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
    if not os.path.exists('development.db'):
        with app.app_context():
            db.create_all()

# Create API instance
api = Api(app, version='1.0', title='HBnB API', description='HBnB application')
api.add_namespace(ns_users)
api.add_namespace(ns_city)
api.add_namespace(ns_country)
api.add_namespace(ns_places)
api.add_namespace(ns_reviews)
api.add_namespace(ns_amenities)

# Ensure all models are created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_admin_user()
    app.run(debug=True)
