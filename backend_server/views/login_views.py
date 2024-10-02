from flask import Blueprint, request, session, g, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect


from backend_server import db
from backend_server.models import User

bp = Blueprint('login_views', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result": "fail"}
    if request.method == 'POST':
        data = request.json
        username = data['username']
        email = data['email']
        pwd = data['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(username=username, password=generate_password_hash(pwd), email=email)
            db.session.add(user)
            db.session.commit()
            status["result"] = "success"


    return status


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

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
            status["name"] = user.username


        response = make_response(status, 200)
        return response


@bp.route(rule='/logout', methods=['GET'])
def logout():
    session.clear()
    status = {"result": "success"}
    return status