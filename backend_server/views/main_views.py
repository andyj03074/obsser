from flask import Blueprint, session, jsonify

bp = Blueprint('main', __name__)

from backend_server.models import User

@bp.route('/')
def home():
    '''if 'username' in session:
        name = session['username']
        return name + " welcome"


    return "login please"'''
    username = "andyj03074"
    user = User.query.filter_by(username=username).first()
    return jsonify(type(user))