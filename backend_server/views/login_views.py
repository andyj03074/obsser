from flask import Blueprint, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect


from backend_server import db
from backend_server.models import User

bp = Blueprint('login_views', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['POST'])
def signup():
    status = {"result": "fail"}
    if request.method == 'POST':
        data = request.json
        username = data['username']
        email = data['email']
        pwd = data['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, password=generate_password_hash(pwd), email=email)
            db.session.add(user)
            db.session.commit()
            status["result"] = "success"

    return status


@bp.route('/login', methods=['POST'])
def login():
    status = {"result": "fail"}
    if request.method == 'POST':
        data = request.json
        email = data['email']
        user = User.query.filter_by(email=email).first()
        pwd_receive = data['password']
        if user is not None and check_password_hash(user.password, pwd_receive):
            session.clear()
            session['email'] = user.email
            status["result"] = "success"

    return status


