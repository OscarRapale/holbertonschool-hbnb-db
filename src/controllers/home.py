from flask import jsonify

def home():
    return jsonify({"msg": "Welcome to the HBnB App!"}), 200
