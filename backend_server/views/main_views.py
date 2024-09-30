from flask import Blueprint, session, jsonify

bp = Blueprint('main', __name__)

from backend_server.models import User

@bp.route('/')
def home():
    return None