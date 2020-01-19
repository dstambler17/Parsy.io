import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.helpSession.utils import *
from flaskApp.error.error_handlers import *
from flaskApp.helpers import getOHData
import json

helpSession = Blueprint('helpSession', __name__)

'''Deletes everything for that course and then adds all'''
@helpSession.route('/restoreOH/<calID>/<courseID>', methods=['POST'])
def restore_office_hours(calID, courseID):
    try:
        DbHelpSessionUtils.restore_all_original_OH(calID, courseID)
        return jsonify({"restore" : "success"}), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@helpSession.route('/getOH/<calID>/<courseID>/<office_hour>', methods=['GET'])
def get_OH_details(calID, courseID, office_hour):
    try:
        res = DbHelpSessionUtils.get_OH_slot_details(calID, courseID, office_hour)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

'''Body takes in a list of time slots to remove, can also take a var that says remove all'''
@helpSession.route('/deleteOH/<calID>/<courseID>', methods=['DELETE'])
def delete_OH(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbHelpSessionUtils.delete_OH_slot(calID, courseID, request_body)
        return jsonify({}), 204
    except (NotFound, BadRequest) as e:
        return jsonify(e.body), e.status_code

'''Body takes in a list of time slots to add, can also take a var that says add all'''
@helpSession.route('addOH/<calID>/<courseID>', methods=['POST'])
def add_OH(calID, courseID):
    try:
        request_body = json.loads(request.get_data())
        DbHelpSessionUtils.add_OH_slot(calID, courseID, request_body)
        return jsonify({}), 201
    except (NotFound, BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

'''Old Method, keep just in case. Will prob be moved to seperate API designed to
interact with just the MySQL database that the data pipeline will drop stuff into'''
@helpSession.route('/getTest/<courseName>', methods=['GET'])
def get_session(courseName):
    try:
        param = courseName #"EN.601.345 Spring 2019"
        result = getOHData(param)
        return jsonify(result)
    except (NotFound) as e:
        return jsonify(e.body), e.status_code
    '''return jsonify({
   "id":"215.215",
   "name":"Intro to Spanish",
   "prof":"Dr. Kaisen",
   "support":[
      {
         "type":"prof",
         "times":"monday 1:00pm-2:00pm, Wednesdays 3:00pm-4:00pm",
         "location":"Olin 274"
      },
      {
         "type":"TA",
         "times":"Friday 12:00pm-2:00pm, Thursdays 3:00pm-4:00pm",
         "location":"Malone 218"
      },
      {
         "type":"Learning den",
         "times":"Tuesday 1:00pm-2:00pm, Wednesdays 3:00pm-4:00pm",
         "location":"Hodson 235"
      }
   ]
}) '''
