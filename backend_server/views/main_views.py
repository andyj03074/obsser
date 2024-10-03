from flask import Blueprint, session, jsonify, request
import base64

bp = Blueprint('main', __name__)

from backend_server.models import User, Bulletin, BulletinComment
from backend_server import db


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


@bp.route(rule='/', methods=['POST'])
def bulletin():
    if request.method == "OPTIONS":
        return '', 200

    data = request.json
    placename = data['placename']
    date = data['date']
    memo = data['memo']
    encoded_image = data['image']
    image_name = data['image_name']
    file_path = "images/" + image_name
    image_data = base64.b64decode(encoded_image)
    with open(file_path, "wb") as file:
        file.write(image_data)

    bulletin = Bulletin(placename=placename, date=date, memo=memo, image=file_path)
    db.session.add(bulletin)
    db.session.commit()


@bp.route(rule='/addcomment', methods=['GET'])
def add_comment():







