from itertools import product
from multiprocessing.dummy import current_process

from flask import Blueprint, request, session
import base64
import requests
import random

from sqlalchemy.sql.expression import func
from backend_server.models import PlaceInfo, User, ProductInfo
from backend_server import db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('place_page_views', __name__, url_prefix='/place_pages')


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


#태그별 장소 상세 설명 페이지
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


@bp.route('/type/<string:type>', methods=['GET'])
def place_page_types(type):
    if request.method == 'OPTIONS':
        return '', 200

    data = {}
    data_list = []

    places = PlaceInfo.query.filter_by(type=type).all()
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
    place = PlaceInfo(name=name, type=type, tag=tag, description=description, image=image)
    db.session.add(place)
    db.session.commit()
    li = PlaceInfo.query.all()
    data = {"len": len(li)}
    return data


#장소 업로드 코드
@bp.route('/add', methods=['POST'])
@jwt_required()
def place_add():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result": "success"}
    data = request.json
    name = data['name']
    type = data['type']
    tag = data['tag']
    description = data['description']
    encoded_image = data['image']
    image_name = data['image_name']
    file_path = "images/" + image_name
    image_data = base64.b64decode(encoded_image)
    with open(file_path, "wb") as file:
        file.write(image_data)

    place = PlaceInfo(name=name, type=type, tag=tag, description=description, image=file_path)
    db.session.add(place)
    db.session.commit()

    return status




def get_weather():
    api_key = "72f2f6d71ad04fb4990151102240310"
    city = "Jeju"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ko"

    response = requests.get(url)
    data = response.json()

    # 날씨 상태 확인
    weather_condition = data['current']['condition']['text']
    return weather_condition


#날씨별 장소 추천
@bp.route('/', methods=['GET'])
def recommended_places():
    if request.method == 'OPTIONS':
        return '', 200

    keywords = {
        "맑음": ['휴양지', '촬영지', '야경'],
        "흐림": ['감성적인', '한적한', '여유로운'],
        "비": ['드라이브', '술', '맛집']
    }
    new_data = {}
    data = {}

    current_weather = get_weather()

    if current_weather in keywords:
        recommended_keyword = random.choice(keywords[current_weather])
        place = PlaceInfo.query.filter_by(tag=recommended_keyword).first()
        data['current_weather'] = current_weather
        data['name'] = place.name
        encoded_image = img_encode(place.image)
        data['image'] = encoded_image
        new_data['data'] = data

        return new_data

    else:
        random_item = PlaceInfo.query.order_by(func.random()).first()
        data['current_weather'] = current_weather
        data['name'] = random_item.name
        encoded_image = img_encode(random_item.image)
        data['image'] = encoded_image
        new_data['data'] = data

        return new_data