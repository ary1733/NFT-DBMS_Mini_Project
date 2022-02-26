from flask import Blueprint
from .user import user_bp
from .item import item_bp
base_bp = Blueprint('base', __name__)
base_bp.register_blueprint(user_bp,  url_prefix="/user")
base_bp.register_blueprint(item_bp, url_prefix="/item")