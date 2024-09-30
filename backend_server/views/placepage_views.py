from flask import Blueprint, request, session


from backend_server.models import PlaceInfo, User
from backend_server import db

bp = Blueprint('place_page_views', __name__, url_prefix='/place_pages')


@bp.route('/<string:tags>', methods=['GET'])
def place_pages(tags):
    data = {}
    name_data = []
    type_data = []
    if request.method == 'GET':
        places = PlaceInfo.query.filter_by(tag=tags).all()
        for place in places:
            name_data.append(place.name)
            type_data.append(place.type)

        data["names"] = name_data
        data["types"] = type_data

    return data


