from flask import Blueprint
from .user import user_bp
base_bp = Blueprint('base', __name__)
base_bp.register_blueprint(user_bp,  url_prefix="/user")