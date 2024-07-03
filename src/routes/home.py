
from flask import Blueprint
from src.controllers.home import home

home_bp = Blueprint("home", __name__)

home_bp.route("/")(home)
