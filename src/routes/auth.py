# src/routes/auth_routes.py
from flask import Blueprint
from src.controllers.auth import login

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/login', methods=['POST'])(login)
