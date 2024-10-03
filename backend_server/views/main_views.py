from flask import Blueprint, session, jsonify, request
import base64
from sqlalchemy.sql.expression import func
import random

bp = Blueprint('main', __name__)

from backend_server.models import User, Bulletin, BulletinComment
from backend_server import db


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image

#홈화면에 3개 랜덤으로 띄움
@bp.route(rule='/', methods=['GET'])
def get_bulletins():
    if request.method == "OPTIONS":
        return '', 200


    data = {}
    data_list = []
    bulletin_list = Bulletin.query.filter_by(func.random()).limit(3).all()

    for bulletin in bulletin_list:
        bl = {}
        bl['name'] = bulletin.placename
        bl['image'] = img_encode(bulletin.image)
        data_list.append(bl)

    data['data'] = data_list

    return data


#게시물 추가
@bp.route(rule='/addbulletin', methods=['POST'])
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


#답글 추가
@bp.route(rule='/<string:placename>', methods=['POST'])
def add_comment(placename):
    if request.method == "OPTIONS":
        return '', 200

    data = request.json
    bulletin = Bulletin.query.filter_by(placename=placename).first()
    comment = data['comment']
    bulletin_comment = BulletinComment(content=comment, bulletin=bulletin)
    db.session.add(bulletin_comment)
    db.session.commit()