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

# Create API instance
api = Api(app, version='1.0', title='HBnB API', description='HBnB application')
api.add_namespace(ns_users)
api.add_namespace(ns_city)
api.add_namespace(ns_country)
api.add_namespace(ns_places)
api.add_namespace(ns_reviews)
api.add_namespace(ns_amenities)

# Create the development database if it doesn't exist
with app.app_context():
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        if not os.path.exists('development.db'):
            db.create_all()

# Routes for HTML pages
@app.route('/index')
def home():
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/place')
def place():
    return app.send_static_file('place.html')

@app.route('/add_review')
def add_review():
    return app.send_static_file('add_review.html')

@app.route('/place_beach')
def place_beach():
    return app.send_static_file('place_beach.html')

@app.route('/place_cozy')
def place_cozy():
    return app.send_static_file('place_cozy.html')

@app.route('/place_modern')
def place_modern():
    return app.send_static_file('place_modern.html')

if __name__ == '__main__':
    with app.app_context():
        create_admin_user()
    app.run(debug=True)
