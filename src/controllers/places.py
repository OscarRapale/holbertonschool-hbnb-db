"""
Places controller module
"""

from flask import abort, request
from src.models import db
from src.models.place import Place
from src.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity


def get_places():
    """Returns all places"""
    places: list[Place] = Place.get_all()

    return [place.to_dict() for place in places], 200

@jwt_required()
def create_place():
    """Creates a new place"""
    data = request.get_json()
    current_user_id = get_jwt_identity()

    # Add the current user as the host of the place
    data['host_id'] = current_user_id

    try:
        place = Place.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(404, str(e))

    return place.to_dict(), 201

def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    place: Place | None = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200


def update_place(place_id: str):
    """Updates a place by ID"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)
    place = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    # Check if the current user is admin or the owner of the place
    if not current_user.is_admin and place.host_id != current_user_id:
        abort(403, "You are not authorized to update this place.")

    try:
        place: Place | None = Place.update(place_id, data)
    except ValueError as e:
        abort(400, str(e))


    return place.to_dict(), 200

@jwt_required()
def delete_place(place_id: str):
    """Deletes a place by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)
    place = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    # Check if the current user is admin or the owner of the place
    if not current_user.is_admin and place.host_id != current_user_id:
        abort(403, "You are not authorized to delete this place.")

    if not Place.delete(place_id):
        abort(404, f"Place with ID {place_id} not found")

    return "", 204
