import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.assignment.utils import *
from flaskApp.error.error_handlers import *
import json
from flaskApp.helpers import getAssignmentData

assignment = Blueprint('assignment', __name__)

@assignment.route('/restoreAssignment/<calID>/<courseID>', methods=['POST'])
def restore_assignment(calID, courseID):
    try:
        DbAssignmentUtils.restore_all_original_assignment(calID, courseID)
        return jsonify({"restore" : "success"}), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@assignment.route('/getAssignment/<calID>/<courseID>/<assignment>', methods=['GET'])
def get_assignment_details(calID, courseID, assignment):
    try:
        res = DbAssignmentUtils.get_assignment_slot_details(calID, courseID, assignment)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@assignment.route('/deleteAssignment/<calID>/<courseID>', methods=['DELETE'])
def delete_assignment(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbAssignmentUtils.delete_assignment_slot(calID, courseID, request_body)
        return jsonify({}), 204
    except (NotFound, BadRequest) as e:
        return jsonify(e.body), e.status_code

@assignment.route('/addAssignment/<calID>/<courseID>', methods=['POST'])
def add_assignment(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        res = DbAssignmentUtils.add_Assignment_slot(calID, courseID, request_body)
        return jsonify(res), 201
    except (NotFound, BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

'''Test method, keep just in case. Will prob be moved to seperate API designed to
interact with just the MySQL database that the data pipeline will drop stuff into'''
@assignment.route('/getAssignmentTest/<courseID>', methods=['GET'])
def get_session_assignment(courseID):
    try:
        result = getAssignmentData(courseID)
        return jsonify(result)
    except (NotFound) as e:
        return jsonify(e.body), e.status_code
