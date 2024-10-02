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


@bp.route('/<string:tags>', methods=['GET'])
def place_pages(tags):
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    name_data = []
    type_data = []
    image_data = []

    if request.method == 'GET':
        places = PlaceInfo.query.filter_by(tag=tags).all()
        for place in places:
            name_data.append(place.name)
            type_data.append(place.type)
            file_path = place.image
            encoded_image = img_encode(file_path)
            image_data.append(encoded_image)


        data["names"] = name_data
        data["types"] = type_data
        data["images"] = image_data


    return data


@bp.route('/', methods=['POST'])
def place_page():
    data = request.json
    name = data['name']
    type = data['type']
    tag = data['tag']
    description = data['description']
    image = data['image']
    product = ProductInfo(name=name, type=type, tag=tag, description=description, image=image)
    db.session.add(product)
    db.session.commit()
    li = ProductInfo.query.all()

    return len(li)