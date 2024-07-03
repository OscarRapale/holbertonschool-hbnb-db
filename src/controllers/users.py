"""
Users controller module
"""

from flask import abort, request
from src.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from src.persistence import repo
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

def get_users():
    """Returns all users"""
    try:
        users = User.get_all()
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    return [user.to_dict() for user in users]


def create_user():
    """Creates a new user"""
    data = request.get_json()

    # Ensure the password is provided
    if 'password' not in data:
        abort(400, "Missing password field")

    try:
        user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


@jwt_required()
def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    try:
        user = User.get(user_id)
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


@jwt_required()
def update_user(user_id: str):
    """Updates a user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Check if the current user is admin or updating their own profile
    if not current_user.is_admin and current_user.id != user_id:
        abort(403, "You are not authorized to update this user.")

    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


@jwt_required()
def delete_user(user_id: str):
    """Deletes a user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Check if the current user is admin
    if not current_user.is_admin:
        abort(403, "You are not authorized to delete users.")

    try:
        if not User.delete(user_id):
            abort(404, f"User with ID {user_id} not found")
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    return "", 204

# Admin endpoint to manage users
@jwt_required()
def promote_user_to_admin(user_id: str):
    """Promotes a user to admin status"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)

    # Check if the current user is admin
    if not current_user.is_admin:
        abort(403, "You are not authorized to promote users.")

    try:
        user = User.get(user_id)
        if not user:
            abort(404, f"User with ID {user_id} not found")
        
        user.is_admin = True
        repo.update(user)
    except SQLAlchemyError as e:
        abort(500, f"Database error: {e}")

    return user.to_dict(), 200
