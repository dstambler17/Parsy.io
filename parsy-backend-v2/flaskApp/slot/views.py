import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.slot.utils import *
from flaskApp.error.error_handlers import *
import json
from flaskApp.helpers import getAssignmentData, getClassMeetingData, getOHData, getExamData

slot = Blueprint('slot', __name__)

@slot.route('/restoreSlot/<calID>/<courseID>', methods=['POST'])
def restore_slot(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbSlotInteract.restore_all_original_slot(calID, courseID, request_body['type'])
        return jsonify({"restore" : "success"}), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@slot.route('/deleteSlot/<calID>/<courseID>', methods=['DELETE'])
def delete_slot(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbSlotInteract.delete_slot(calID, courseID, request_body)
        return jsonify({}), 204
    except (NotFound, BadRequest) as e:
        return jsonify(e.body), e.status_code

@slot.route('/addSlot/<calID>/<courseID>', methods=['POST'])
def add_slot(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        res = DbSlotInteract.add_slot(calID, courseID, request_body)
        return jsonify(res), 201
    except (NotFound, BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@slot.route('/getSlot/<calID>/<courseID>/<slot>', methods=['GET'])
def get_slot_details(calID, courseID, slot):
    try:
        res = DbSlotInteract.get_slot_details(calID, courseID, slot)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

'''Test method, keep just in case. Will prob be moved to seperate API designed to
interact with just the MySQL database that the data pipeline will drop stuff into'''
@slot.route('/getSlotTest/<courseID>', methods=['GET'])
def get_session_slot(courseID):
    try:
        result = getSlotData(courseID)
        return jsonify(result)
    except (NotFound) as e:
        return jsonify(e.body), e.status_code
