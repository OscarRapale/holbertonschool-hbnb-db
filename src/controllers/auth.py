# src/controllers/auth_controller.py
from flask import request, jsonify, abort
from flask_jwt_extended import create_access_token
from src.models.user import User

def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        abort(400, "Missing email or password")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'email': user.email, 'is_admin': user.is_admin})
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401
