from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

@jwt_required()
def admin_data():
    """
    Provide admin data.

    This function is protected by the jwt_required decorator, meaning it requires a valid JWT 
    in the request headers. It retrieves the JWT claims and checks if the 'is_admin' claim is present 
    and true. If not, it returns a 403 Forbidden response. If the 'is_admin' claim is present and true, 
    it proceeds with admin-only functionality and returns a 200 OK response.

    Returns:
        A tuple containing a JSON response and a status code. The JSON response contains a message 
        indicating whether admin access was granted or not. The status code is 200 if admin access 
        was granted, or 403 if it wasn't.
    """
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    # Proceed with admin-only functionality
    return jsonify({"msg": "Admin access granted"}), 200
