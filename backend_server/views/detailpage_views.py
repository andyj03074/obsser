from flask import Blueprint, request, session

from backend_server import db
from backend_server.models import ProductInfo, User, PlaceInfo
import base64
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('detail', __name__, url_prefix='/detail')


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


#상품 상세 페이지
@bp.route('/<string:detail_name>', methods=['GET'])
def detail(detail_name):
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    if request.method == 'GET':
        product = ProductInfo.query.filter_by(name=detail_name).first_or_404()
        file_path = product.image

        encoded_image = img_encode(file_path)
        data = {
            "price": product.price,
            "description": product.description,
            "image": encoded_image,
        }

        return data


#상품 찜 목록에 상품 추가
@bp.route('/<string:detail_name>/like', methods=['GET'])
@jwt_required()
def add_myproduct(detail_name):
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result" : "success"}
    current_user = get_jwt_identity()
    email = current_user['email']
    user = User.query.filter_by(email=email).first()
    product = ProductInfo.query.filter_by(name=detail_name).first_or_404()
    if product not in user.myproducts:
        user.myproducts.append(product)
        db.session.commit()
        return status

    status["result"] = "fail"
    return status


#임시 업로드
@bp.route('/', methods=['POST'])
def upload():
    data = request.json
    name = data['name']
    price = data['price']
    description = data['description']
    image = data['image']
    product = ProductInfo(name=name, price=price, description=description, image=image)
    db.session.add(product)
    db.session.commit()
    li = ProductInfo.query.all()
    data = {"len": len(li)}
    return data