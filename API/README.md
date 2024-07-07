# API Directory

Welcome to the API directory for the `holbertonschool-hbnb` project. This directory contains the implementation of RESTful endpoints for managing various entities within the application. Below, you will find information on the available endpoints, their usage, and the required data formats.

## Table of Contents

- [User Management Endpoints](#user-management-endpoints)
- [Country and City Management Endpoints](#country-and-city-management-endpoints)
- [Amenity Management Endpoints](#amenity-management-endpoints)
- [Places Management Endpoints](#places-management-endpoints)
- [Review Management Endpoints](#review-management-endpoints)

## User Management Endpoints

### POST /users
Create a new user.

#### Request
- JSON payload with the following fields:
  - `email`: string (unique, valid email format)
  - `first_name`: string (non-empty)
  - `last_name`: string (non-empty)

#### Response
- `201 Created`: Successfully created a new user.

### GET /users
Retrieve a list of all users.

#### Response
- `200 OK`: List of all users.

### GET /users/{user_id}
Retrieve details of a specific user.

#### Response
- `200 OK`: User details.
- `404 Not Found`: User not found.

### PUT /users/{user_id}
Update an existing user.

#### Request
- JSON payload with the following fields:
  - `email`: string (unique, valid email format)
  - `first_name`: string (non-empty)
  - `last_name`: string (non-empty)

#### Response
- `200 OK`: Successfully updated the user.
- `404 Not Found`: User not found.

### DELETE /users/{user_id}
Delete a user.

#### Response
- `204 No Content`: Successfully deleted the user.
- `404 Not Found`: User not found.

## Country and City Management Endpoints

### GET /countries
Retrieve all pre-loaded countries.

#### Response
- `200 OK`: List of all countries.

### GET /countries/{country_code}
Retrieve details of a specific country by its code.

#### Response
- `200 OK`: Country details.
- `404 Not Found`: Country not found.

### GET /countries/{country_code}/cities
Retrieve all cities belonging to a specific country.

#### Response
- `200 OK`: List of all cities in the specified country.
- `404 Not Found`: Country not found.

### POST /cities
Create a new city.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty, unique within the country)
  - `country_code`: string (valid country code)

#### Response
- `201 Created`: Successfully created a new city.

### GET /cities
Retrieve all cities.

#### Response
- `200 OK`: List of all cities.

### GET /cities/{city_id}
Retrieve details of a specific city.

#### Response
- `200 OK`: City details.
- `404 Not Found`: City not found.

### PUT /cities/{city_id}
Update an existing city.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty, unique within the country)
  - `country_code`: string (valid country code)

#### Response
- `200 OK`: Successfully updated the city.
- `404 Not Found`: City not found.

### DELETE /cities/{city_id}
Delete a city.

#### Response
- `204 No Content`: Successfully deleted the city.
- `404 Not Found`: City not found.

## Amenity Management Endpoints

### POST /amenities
Create a new amenity.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty, unique)

#### Response
- `201 Created`: Successfully created a new amenity.

### GET /amenities
Retrieve a list of all amenities.

#### Response
- `200 OK`: List of all amenities.

### GET /amenities/{amenity_id}
Retrieve detailed information about a specific amenity.

#### Response
- `200 OK`: Amenity details.
- `404 Not Found`: Amenity not found.

### PUT /amenities/{amenity_id}
Update an existing amenity.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty, unique)

#### Response
- `200 OK`: Successfully updated the amenity.
- `404 Not Found`: Amenity not found.

### DELETE /amenities/{amenity_id}
Delete a specific amenity.

#### Response
- `204 No Content`: Successfully deleted the amenity.
- `404 Not Found`: Amenity not found.

## Places Management Endpoints

### POST /places
Create a new place.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty)
  - `description`: string
  - `address`: string
  - `city_id`: string (valid city ID)
  - `latitude`: float
  - `longitude`: float
  - `host_id`: string (valid user ID)
  - `number_of_rooms`: int (non-negative)
  - `number_of_bathrooms`: int (non-negative)
  - `price_per_night`: float (non-negative)
  - `max_guests`: int (non-negative)
  - `amenity_ids`: list of strings (valid amenity IDs)

#### Response
- `201 Created`: Successfully created a new place.

### GET /places
Retrieve a list of all places.

#### Response
- `200 OK`: List of all places.

### GET /places/{place_id}
Retrieve detailed information about a specific place.

#### Response
- `200 OK`: Place details.
- `404 Not Found`: Place not found.

### PUT /places/{place_id}
Update an existing place.

#### Request
- JSON payload with the following fields:
  - `name`: string (non-empty)
  - `description`: string
  - `address`: string
  - `city_id`: string (valid city ID)
  - `latitude`: float
  - `longitude`: float
  - `host_id`: string (valid user ID)
  - `number_of_rooms`: int (non-negative)
  - `number_of_bathrooms`: int (non-negative)
  - `price_per_night`: float (non-negative)
  - `max_guests`: int (non-negative)
  - `amenity_ids`: list of strings (valid amenity IDs)

#### Response
- `200 OK`: Successfully updated the place.
- `404 Not Found`: Place not found.

### DELETE /places/{place_id}
Delete a specific place.

#### Response
- `204 No Content`: Successfully deleted the place.
- `404 Not Found`: Place not found.

## Review Management Endpoints

### POST /places/{place_id}/reviews
Create a new review for a specified place.

#### Request
- JSON payload with the following fields:
  - `user_id`: string (valid user ID)
  - `rating`: int (1-5)
  - `comment`: string

#### Response
- `201 Created`: Successfully created a new review.

### GET /users/{user_id}/reviews
Retrieve all reviews written by a specific user.

#### Response
- `200 OK`: List of all reviews by the user.
- `404 Not Found`: User not found.

### GET /places/{place_id}/reviews
Retrieve all reviews for a specific place.

#### Response
- `200 OK`: List of all reviews for the place.
- `404 Not Found`: Place not found.

### GET /reviews/{review_id}
Retrieve detailed information about a specific review.

#### Response
- `200 OK`: Review details.
- `404 Not Found`: Review not found.

### PUT /reviews/{review_id}
Update an existing review.

#### Request
- JSON payload with the following fields:
  - `user_id`: string (valid user ID)
  - `rating`: int (1-5)
  - `comment`: string

#### Response
- `200 OK`: Successfully updated the review.
- `404 Not Found`: Review not found.

### DELETE /reviews/{review_id}
Delete a specific review.

#### Response
- `204 No Content`: Successfully deleted the review.
- `404 Not Found`: Review not found.
