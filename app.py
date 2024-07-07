#!/usr/bin/python3
import os
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from API.api_users import ns_users
from API.api_country_city import ns_country, ns_city
from API.api_places import ns_places
from API.api_reviews import ns_reviews
from API.api_amenity import ns_amenities
from flask_jwt_extended import JWTManager
from create_admin import create_admin_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'aminarufatrafig'
jwt = JWTManager(app)

if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
    if not os.path.exists('development.db'):
        with app.app_context():
            db.create_all()


api = Api(app, version='1.0', title='HBnB API', description='HBnB application')
api.add_namespace(ns_users)
api.add_namespace(ns_city)
api.add_namespace(ns_country)
api.add_namespace(ns_places)
api.add_namespace(ns_reviews)
api.add_namespace(ns_amenities)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    create_admin_user()
    app.run(debug=True)
