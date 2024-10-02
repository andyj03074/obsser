from itertools import product

from flask import Blueprint, request, session
import base64

from backend_server.models import PlaceInfo, User, ProductInfo
from backend_server import db

bp = Blueprint('place_page_views', __name__, url_prefix='/place_pages')


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


#장소 상세 설명 페이지
@bp.route('/<string:tags>', methods=['GET'])
def place_pages(tags):
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    data_list = []

    if request.method == 'GET':
        places = PlaceInfo.query.filter_by(tag=tags).all()
        for place in places:
            pl = {}
            pl['name'] = place.name
            file_path = place.image
            encoded_image = img_encode(file_path)
            pl['image'] = encoded_image
            data_list.append(pl)

    data['data'] = data_list

    return data


#임시 업로드 코드
@bp.route('/', methods=['POST'])
def place_page():
    data = request.json
    name = data['name']
    type = data['type']
    tag = data['tag']
    description = data['description']
    image = data['image']
    product = PlaceInfo(name=name, type=type, tag=tag, description=description, image=image)
    db.session.add(product)
    db.session.commit()
    li = ProductInfo.query.all()
    data = {"len": len(li)}
    return data


#업로드 코드
@bp.route('/add', methods=['POST'])
def place_add():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = request.json
    name = data['name']
    type = data['type']
    tag = data['tag']
    description = data['description']
    image = data['image']
    image_name = data['image_name']