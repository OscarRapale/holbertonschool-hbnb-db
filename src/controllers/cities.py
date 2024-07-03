"""
Cities controller module
"""

from flask import request, abort, jsonify
from src.models.city import City
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def get_cities():
    """Returns all cities"""
    cities: list[City] = City.get_all()

    return [city.to_dict() for city in cities]

@jwt_required()
def create_city():
    """Creates a new city"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()

    try:
        city = City.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return city.to_dict(), 201

@jwt_required()
def get_city_by_id(city_id: str):
    """Returns a city by ID"""
    city: City | None = City.get(city_id)

    if not city:
        abort(404, f"City with ID {city_id} not found")

    return city.to_dict()

@jwt_required()
def update_city(city_id: str):
    """Updates a city by ID"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    data = request.get_json()

    try:
        city: City | None = City.update(city_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not city:
        abort(404, f"City with ID {city_id} not found")

    return city.to_dict()

@jwt_required()
def delete_city(city_id: str):
    """Deletes a city by ID"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    
    if not City.delete(city_id):
        abort(404, f"City with ID {city_id} not found")

    return "", 204
