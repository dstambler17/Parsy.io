import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.classMeeting.utils import *
from flaskApp.error.error_handlers import *
from flaskApp.helpers import getExamData
import json

classMeeting = Blueprint('classMeeting', __name__)
@classMeeting.route('/restoreClassMeeting/<calID>/<courseID>', methods=['POST'])
def restore_meeting_time(calID, courseID):
    try:
        DbClassMeetingUtils.restore_all_original_class_meeting(calID, courseID)
        return jsonify({"restore" : "success"}), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@classMeeting.route('/getClassMeeting/<calID>/<courseID>/<meeting_time>', methods=['GET'])
def get_meeting_time(calID, courseID, meeting_time):
    try:
        res = DbClassMeetingUtils.get_class_meeting_slot_details(calID, courseID, meeting_time)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@classMeeting.route('/deleteClassMeeting/<calID>/<courseID>', methods=['DELETE'])
def delete_meeting_time(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbClassMeetingUtils.delete_class_meeting_slot(calID, courseID, request_body)
        return jsonify({}), 204
    except (NotFound, BadRequest) as e:
        return jsonify(e.body), e.status_code

@classMeeting.route('addClassMeeting/<calID>/<courseID>', methods=['POST'])
def add_meeting_time(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        res = DbClassMeetingUtils.add_class_meeting_slot(calID, courseID, request_body)
        return jsonify(res), 201
    except (NotFound, BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

''''Test method, keep just in case. Will prob be moved to seperate API designed to
interact with just the MySQL database that the data pipeline will drop stuff into'''
@classMeeting.route('/getClassMeetingTest/<courseID>', methods=['GET'])
def get_session_classMeeting(courseID):
    try:
        result = getClassMeetingData(courseID)
        return jsonify(result)
    except (NotFound) as e:
        return jsonify(e.body), e.status_code
