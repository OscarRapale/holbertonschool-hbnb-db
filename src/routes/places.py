"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
    add_amenity_to_place,
    get_amenities_of_place
)

places_bp = Blueprint("places", __name__, url_prefix="/places")

places_bp.route("/", methods=["GET"])(get_places)
places_bp.route("/", methods=["POST"])(create_place)

places_bp.route("/<place_id>", methods=["GET"])(get_place_by_id)
places_bp.route("/<place_id>", methods=["PUT"])(update_place)
places_bp.route("/<place_id>", methods=["DELETE"])(delete_place)
places_bp.route("/<place_id>/amenities", methods=["POST"])(add_amenity_to_place)
places_bp.route("/<place_id>/amenities", methods=["GET"])(get_amenities_of_place)
