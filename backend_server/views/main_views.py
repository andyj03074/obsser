from flask import Blueprint, session, jsonify
import base64

bp = Blueprint('main', __name__)

from backend_server.models import User

@bp.route('/')
def home():
    return None


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image

