from flask import Blueprint, session, request

from backend_server.models import User, Notice, Inquiry
from backend_server import db
import base64


bp = Blueprint('mypage_views', __name__, url_prefix='/mypage')


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


@bp.route('/mypruduct', methods=['GET'])
def my_product():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    price =[]
    name = []
    description = []
    image_list = []
    email = session['email']
    user = User.query.filter_by(email=email).first()
    myproduct_list = user.myproduct_list
    for myproduct in myproduct_list:
        price.append(myproduct.price)
        name.append(myproduct.name)
        description.append(myproduct.description)
        file_path = myproduct.image
        encoded_image = img_encode(file_path)
        image_list.append(encoded_image)


    data['price'] = price
    data['name'] = name
    data['description'] = description
    data['image_list'] = image_list


    return data


@bp.route('/notice', methods=['GET'])
def _notice():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    description = []
    recent_notice = Notice.query.order_by(Notice.id.desc()).limit(5)
    for notice in recent_notice:
        description.append(notice.description)

    data['description'] = description

    return data


@bp.route('/myinquiry', methods=['GET'])
def my_inquiry():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    title = []
    content = []
    email = session['email']
    user = User.query.filter_by(email=email).first()
    inquiry_list = user.inquiry_list
    for inquiry in inquiry_list:
        title.append(inquiry.title)
        content.append(inquiry.content)

    data['title'] = title
    data['content'] = content

    return data


@bp.route('/addinquiry', methods=['POST'])
def add_inquiry():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result" : "success"}
    data = request.json
    title = data['title']
    content = data['content']
    email = session['email']
    user = User.query.filter_by(email=email).first()

    inquiry = Inquiry(title=title, content=content)
    db.session.add(inquiry)
    db.session.commit()

    inquiry = Inquiry.query.filter_by(title=title).first()

    user.inquiry_list.append(inquiry)
    db.session.commit()
    return status

