"""
Reviews controller module
"""

from flask import abort, request
from src.models.review import Review
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User

@jwt_required()
def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()

    return [review.to_dict() for review in reviews], 200

@jwt_required()
def create_review(place_id: str):
    """Creates a new review"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    data["user_id"] = current_user_id  # Ensure the review is created by the current user

    try:
        review = Review.create(data | {"place_id": place_id})
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return review.to_dict(), 201

@jwt_required()
def get_reviews_from_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews = Review.get_all()

    return [
        review.to_dict() for review in reviews if review.place_id == place_id
    ], 200

@jwt_required()
def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews = Review.get_all()

    return [
        review.to_dict() for review in reviews if review.user_id == user_id
    ], 200

@jwt_required()
def get_review_by_id(review_id: str):
    """Returns a review by ID"""
    review: Review | None = Review.get(review_id)

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    return review.to_dict(), 200

@jwt_required()
def update_review(review_id: str):
    """Updates a review by ID"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    review = Review.get(review_id)

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    # Only allow the user who created the review or an admin to update it
    if review.user_id != current_user_id and not User.get(current_user_id).is_admin:
        abort(403, "You are not authorized to update this review.")

    try:
        review: Review | None = Review.update(review_id, data)
    except ValueError as e:
        abort(400, str(e))

    return review.to_dict(), 200

@jwt_required()
def delete_review(review_id: str):
    """Deletes a review by ID"""
    current_user_id = get_jwt_identity()
    review = Review.get(review_id)

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    # Only allow the user who created the review or an admin to delete it
    if review.user_id != current_user_id and not User.get(current_user_id).is_admin:
        abort(403, "You are not authorized to delete this review.")

    Review.delete(review_id)

    return "", 204
