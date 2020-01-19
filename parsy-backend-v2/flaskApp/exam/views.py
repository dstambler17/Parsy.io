import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.exam.utils import *
from flaskApp.error.error_handlers import *
import json
from flaskApp.helpers import getExamData

exam = Blueprint('exam', __name__)

@exam.route('/restoreExam/<calID>/<courseID>', methods=['POST'])
def restore_exam(calID, courseID):
    try:
        DbExamUtils.restore_all_original_exam(calID, courseID)
        return jsonify({"restore" : "success"}), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@exam.route('/getExam/<calID>/<courseID>/<exam>', methods=['GET'])
def get_exam_details(calID, courseID, exam):
    try:
        res = DbExamUtils.get_exam_slot_details(calID, courseID, exam)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@exam.route('/deleteExam/<calID>/<courseID>', methods=['DELETE'])
def delete_exam(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbExamUtils.delete_exam_slot(calID, courseID, request_body)
        return jsonify({}), 204
    except (NotFound, BadRequest) as e:
        return jsonify(e.body), e.status_code

@exam.route('/addExam/<calID>/<courseID>', methods=['POST'])
def add_exam(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        res = DbExamUtils.add_Exam_slot(calID, courseID, request_body)
        return jsonify(res), 201
    except (NotFound, BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

'''Test method, keep just in case. Will prob be moved to seperate API designed to
interact with just the MySQL database that the data pipeline will drop stuff into'''
@exam.route('/getExamTest/<courseID>', methods=['GET'])
def get_session_exam(courseID):
    try:
        result = getExamData(courseID)
        return jsonify(result)
    except (NotFound) as e:
        return jsonify(e.body), e.status_code
