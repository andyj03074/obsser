from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import base64


import config

db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    #ORM Config
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models


    from .views import main_views, login_views, detailpage_views, placepage_views, mytrip_views, mypage_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(login_views.bp)
    app.register_blueprint(detailpage_views.bp)
    app.register_blueprint(placepage_views.bp)
    app.register_blueprint(mytrip_views.bp)
    app.register_blueprint(mypage_views.bp)


    return app
