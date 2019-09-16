import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.course.utils import *
from flaskApp.course.GoogCalInteract import *
from flaskApp.error.error_handlers import *
import json

course = Blueprint('course', __name__)

@course.route('/newCal', methods=['POST'])
def new_session():
    try:
        request_body = json.loads(request.get_data())
        print(str(request_body))
        id = DbCourseitemUtils.creatCal(request_body)
        return jsonify({'id' : str(id)}), 201

    except(BadRequest, NotFound) as e:
        return jsonify(e.body), e.status_code

@course.route('/<calID>', methods=['GET', 'DELETE'])
def get_calender(calID):
    try:
        if request.method == 'DELETE':
            DbCourseitemUtils.delete_cal(calID)
            return jsonify({}), 204
        elif request.method == 'GET':
            res = DbCourseitemUtils.get_cal(calID)
            return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@course.route('saveCal/<calID>', methods=['POST'])
def save_to_GCal(calID):
    try:
        request_body = json.loads(request.get_data())
        res = DbCourseitemUtils.get_cal(calID)
        GCalInteract.export_cal(res, request_body['userid'])
        return jsonify({}), 201
    except (NotFound, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@course.route('/<calID>/addClassHelp/<courseIDSem>', methods=['POST'])
def add_session(calID, courseIDSem):
    try:
        result = DbCourseitemUtils.add_helpTime(calID, courseIDSem)
        return jsonify(result), 201
    except (NotFound, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@course.route('/<calID>/removeClass/<courseID>', methods=['DELETE'])
def delete_session(calID, courseID):
    try:
        DbCourseitemUtils.delete_classHelpTimes(calID, courseID)
        return jsonify({}), 204
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@course.route('/addData', methods=['POST'])
def upload_data():
    try:
        request_body = json.loads(request.get_data())
        DbCourseitemUtils.add_new_data_to_db(request_body)
        return jsonify({}), 201
    except (NotFound, ValidationFailed, BadRequest) as e:
        return jsonify(e.body), e.status_code
