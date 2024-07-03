from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    # Proceed with admin-only functionality
    return jsonify({"msg": "Admin access granted"}), 200
