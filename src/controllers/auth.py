from flask import request, jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def login():
    """
    Log in a user.

    This function handles the login process. It first gets the email and password from the request.
    Then it queries the database for a User with the given email. If a User with the given email exists
    and the given password matches the User's password, it creates an access token for the User and
    returns it. If a User with the given email doesn't exist or the given password doesn't match the
    User's password, it returns a 401 Unauthorized response.

    Returns:
        A tuple containing a JSON response and a status code. The JSON response contains the access
        token if the login was successful, or an error message if it wasn't. The status code is 200
        if the login was successful, or 401 if it wasn't.
    """
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad email or password"}), 401
