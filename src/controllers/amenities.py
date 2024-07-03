"""
Amenity controller module
"""

from flask import abort, request
from src.models.amenity import Amenity
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User


@jwt_required()
def get_amenities():
    """Returns all amenities"""
    amenities: list[Amenity] = Amenity.get_all()

    return [amenity.to_dict() for amenity in amenities]


@jwt_required()
def create_amenity():
    """Creates a new amenity"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Only allow admin users to create amenities
    if not current_user.is_admin:
        abort(403, "You are not authorized to create an amenity.")

    data = request.get_json()

    try:
        amenity = Amenity.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return amenity.to_dict(), 201

@jwt_required()
def get_amenity_by_id(amenity_id: str):
    """Returns a amenity by ID"""
    amenity: Amenity | None = Amenity.get(amenity_id)

    if not amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return amenity.to_dict()

@jwt_required()
def update_amenity(amenity_id: str):
    """Updates a amenity by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Only allow admin users to update amenities
    if not current_user.is_admin:
        abort(403, "You are not authorized to update an amenity.")

    data = request.get_json()

    updated_amenity: Amenity | None = Amenity.update(amenity_id, data)

    if not updated_amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return updated_amenity.to_dict()

@jwt_required()
def delete_amenity(amenity_id: str):
    """Deletes a amenity by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Only allow admin users to delete amenities
    if not current_user.is_admin:
        abort(403, "You are not authorized to delete an amenity.")

    if not Amenity.delete(amenity_id):
        abort(404, f"Amenity with ID {amenity_id} not found")

    return "", 204
