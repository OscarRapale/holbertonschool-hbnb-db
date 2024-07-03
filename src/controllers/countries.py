"""
Countries controller module
"""

from flask import abort, request, jsonify
from src.models.city import City
from src.models.country import Country
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def get_countries():
    """Returns all countries"""
    countries: list[Country] = Country.get_all()

    return [country.to_dict() for country in countries]

@jwt_required()
def get_country_by_code(code: str):
    """Returns a country by code"""
    country: Country | None = Country.get(code)

    if not country:
        abort(404, f"Country with ID {code} not found")

    return country.to_dict()

@jwt_required()
def get_country_cities(code: str):
    """Returns all cities for a specific country by code"""
    country: Country | None = Country.get(code)

    if not country:
        abort(404, f"Country with ID {code} not found")

    cities: list[City] = City.get_all()

    country_cities = [
        city.to_dict() for city in cities if city.country_code == country.code
    ]

    return country_cities

@jwt_required()
def create_country():
    """Creates a new country"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    data = request.get_json()
    try:
        name = data['name']
        code = data['code']
        country = Country.create(name, code)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))
    return country.to_dict(), 201

@jwt_required()
def delete_country(code: str):
    """Deletes a country by code"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    if not Country.delete(code):
        abort(404, f"Country with code {code} not found")
    return "", 204
