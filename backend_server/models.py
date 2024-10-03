from tkinter.constants import CASCADE

from backend_server import db


class TravelPlan(db.Model):
    __tablename__ = 'travelplan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(150), nullable=False)


class PlaceInfo(db.Model):
    __tablename__ = 'placeinfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    tag = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(), nullable=False)


class ProductInfo(db.Model):
    __tablename__ = 'productinfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)


class Inquiry(db.Model):
    __tablename__ = 'inquiry'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)


myplace = db.Table('myplace',db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete = CASCADE), primary_key=True),
                       db.Column('placeinfo_id', db.Integer, db.ForeignKey('placeinfo.id', ondelete = CASCADE), primary_key=True))


mytravel = db.Table('mytravel', db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete = CASCADE), primary_key=True),
                    db.Column('travelplan_id', db.Integer, db.ForeignKey('travelplan.id', ondelete = CASCADE), primary_key=True))


myproduct = db.Table('myproduct', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('productinfo_id', db.Integer, db.ForeignKey('productinfo.id'), primary_key=True))


myinquiry = db.Table('myinquiry', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('inquiryinfo_id', db.Integer, db.ForeignKey('inquiry.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    myplace_list = db.relationship('PlaceInfo', secondary=myplace, backref='myplace')
    mytravel_list = db.relationship('TravelPlan', secondary=mytravel, backref='mytravel')
    myproduct_list = db.relationship('ProductInfo', secondary=myproduct, backref='product')


class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)


class Bulletin(db.Model):
    __tablename__ = 'bulletin'
    id = db.Column(db.Integer, primary_key=True)
    placename = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    memo = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(), nullable=False)


class BulletinComment(db.Model):
    __tablename__ = 'bulletincomment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    bulletin_id = db.Column(db.Integer, db.ForeignKey('bulletin.id'), nullable=False)
    bulletin = db.relationship('Bulletin', backref='comment')
    user = db.relationship('User', backref='bulletin')

