from flask import Blueprint, jsonify, request, session
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from backend_server import db
from backend_server.models import User, PlaceInfo, TravelPlan
import base64
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('mytrip_views', __name__, url_prefix='/mytrip')


def img_encode(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image


#여행계획 추가
@bp.route('/addmytrip', methods=['POST'])
@jwt_required()
def add_mytrip():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result" : "success"}
    data = request.json
    name = data['name']
    date = data['date']
    image_url = data['image_url']
    current_user = get_jwt_identity()
    email = current_user['email']
    user = User.query.filter_by(email=email).first()
    travelplan = TravelPlan(name=name, date=date, image_url=image_url)
    db.session.add(travelplan)
    db.session.commit()

    plan = TravelPlan.query.filter_by(name=name).first()
    if plan not in user.mytravel_list:
        user.mytravel_list.append(plan)
        db.session.commit()
        return status

    status["result"] = "fail"
    return status


#내 장소 찜 목록 불러오기
@bp.route('/myplace', methods=['GET'])
@jwt_required()
def get_myplace():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    namelist = []
    description_list = []
    tags_list = []
    image_list = []
    if request.method == "GET":
        current_user = get_jwt_identity()
        email = current_user['email']
        user = User.query.filter_by(email=email).first()
        myplace_list = user.myplace_list
        for myplace in myplace_list:
            namelist.append(myplace.name)
            description_list.append(myplace.description)
            tags_list.append(myplace.tags)
            file_path = myplace.image
            encoded_image = img_encode(file_path)
            image_list.append(encoded_image)


        data['name'] = namelist
        data['description'] = description_list
        data['tags'] = tags_list
        data['image'] = image_list

        return data


#장소 찜 목록 지우기
@bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_myplace():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result": "success"}
    data = request.json
    del_list = data['delete_table']
    current_user = get_jwt_identity()
    email = current_user['email']
    user = User.query.filter_by(email=email).first()

    for place in del_list:
        del_place = PlaceInfo.query.filter_by(name=place).first()
        if del_place in user.myplace_list:
            user.myplace_list.remove(del_place)
            db.session.commit()
            return status

    status["result"] = "fail"
    return status


#내 여행계획 불러오기
@bp.route(rule='', methods=['GET'])
@jwt_required()
def get_mytrip():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    data = {}
    name_list = []
    date_list = []
    image_url_list = []
    current_user = get_jwt_identity()
    email = current_user['email']
    user = User.query.filter_by(email=email).first()
    travelplan_list = user.mytravel_list
    for travelplan in travelplan_list:
        name_list.append(travelplan.name)
        date_list.append(travelplan.date)
        image_url_list.append(travelplan.image_url)

    data['name'] = name_list
    data['date'] = date_list
    data['image_url'] = image_url_list

    return data


# 장소 찜 목록에 장소 추가
@bp.route('/add', methods=['POST'])
@jwt_required()
def add_myplace():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200

    status = {"result" : "success"}
    data = request.json
    add_list = data['add_table']
    current_user = get_jwt_identity()
    email = current_user['email']
    user = User.query.filter_by(email=email).first()

    for place in add_list:
        add_place = PlaceInfo.query.filter_by(name=place).first()
        if add_place not in user.myplace_list:
            user.myplace_list.append(add_place)
            db.session.commit()
            return status

    status["result"] = "fail"
    return status


def create_data_model(distance_matrix):
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def extract_route(manager, routing, solution):
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    route.append(manager.IndexToNode(index))
    return route


#경로 탐색
@bp.route('/pathfind', methods=['POST'])
@jwt_required()
def pathfind():
    if request.method == 'OPTIONS':
        # Preflight 요청에 대해 200 OK 응답
        return '', 200


    calculated_data = {}
    data = request.json
    distance_matrix = data['distance_matrix']

    data = create_data_model(distance_matrix)

    # TSP 라우팅 모델 생성
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # 비용 계산 콜백 함수 정의
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 탐욕적인 초기 경로로 TSP 해결 설정
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # TSP 문제 해결
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        calculated_data['route'] = extract_route(manager, routing, solution)
        return calculated_data
    else:
        return None