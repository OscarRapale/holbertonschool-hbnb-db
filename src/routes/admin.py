from flask import Blueprint
from src.controllers.admin import admin_data


admin_bp = Blueprint('admin', __name__)

admin_bp.route('/admin/data', methods=['POST', 'DELETE'])(admin_data)


