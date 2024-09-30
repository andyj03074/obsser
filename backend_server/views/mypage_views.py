from flask import Blueprint, session, request

from backend_server.models import User, Notice, Inquiry
from backend_server import db


bp = Blueprint('mypage_views', __name__, url_prefix='/mypage')


@bp.route('/mypruduct', methods=['GET'])
def my_product():
    data = {}
    price =[]
    name = []
    description = []
    email = session['email']
    user = User.query.filter_by(email=email).first()
    myproduct_list = user.myproduct_list
    for myproduct in myproduct_list:
        price.append(myproduct.price)
        name.append(myproduct.name)
        description.append(myproduct.description)

    data['price'] = price
    data['name'] = name
    data['description'] = description

    return data


@bp.route('/notice', methods=['GET'])
def _notice():
    data = {}
    description = []
    recent_notice = Notice.query.order_by(Notice.id.desc()).limit(5)
    for notice in recent_notice:
        description.append(notice.description)

    data['description'] = description

    return data


@bp.route('/myinquiry', methods=['GET'])
def my_inquiry():
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

