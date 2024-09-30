from flask import Blueprint, request, session


from backend_server import db
from backend_server.models import ProductInfo, User, PlaceInfo
import base64


bp = Blueprint('detail', __name__, url_prefix='/detail')


@bp.route('/<string:detail_name>', methods=['GET'])
def detail(detail_name):
    if request.method == 'GET':
        product = ProductInfo.query.filter_by(name=detail_name).first_or_404()
        file_path = product.image

        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            data = {
                "price": product.price,
                "description": product.description,
                "image": encoded_image,
            }

            return data




@bp.route('/<string:detail_name>/like', methods=['GET'])
def add_myproduct(detail_name):
    status = {"result" : "success"}
    email = session['email']
    user = User.query.filter_by(email=email).first()
    product = ProductInfo.query.filter_by(name=detail_name).first_or_404()
    if product not in user.myproducts:
        user.myproducts.append(product)
        db.session.commit()
        return status

    status["result"] = "fail"
    return status


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

file = 'images/banner1.png'
p = ProductInfo(name='제주마음샌드 케이크', price=31350, description='제주마음샌드 케이크를 구매하세요', image=file)