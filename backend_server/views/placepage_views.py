from flask import Blueprint, request, session
from main_views import img_encode

from backend_server.models import PlaceInfo, User
from backend_server import db

bp = Blueprint('place_page_views', __name__, url_prefix='/place_pages')


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


