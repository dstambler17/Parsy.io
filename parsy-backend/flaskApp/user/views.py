import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.user.utils import *
from flaskApp.error.error_handlers import *
import json

user = Blueprint('user', __name__)

@user.route('/new', methods=['POST'])
def new_user():
    try:
        request_body = json.loads(request.get_data())
        DbUserUtils.add_new_user(request_body)
        return jsonify({}), 201
    except (BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code


@user.route('/GSignIn', methods=['POST'])
def user_GAuth_signIn():
    try:
        request_body = json.loads(request.get_data())
        #request_body['creds'] = request.headers.get('Authorization')
        res = DbUserUtils.SignIn_user_gauth(request_body)
        return jsonify(res), 201
    except (BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@user.route('/GSignInPageReload', methods=['POST'])
def user_GAuth_signInAgain():
    try:
        request_body = json.loads(request.get_data())
        request_body['id_token'] = request.headers.get('Authorization')
        res = DbUserUtils.SignIn_user_gauth_already_signedIn(request_body)
        return jsonify(res), 201
    except (BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@user.route('/login', methods=['POST'])
def login():
    try:
        request_body = json.loads(request.get_data())
        DbUserUtils.user_login(request_body)
        return jsonify({}), 201
    except (ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@user.route('/getInfo/<user_name>', methods=['GET'])
def get_user_data(user_name):
    try:
        res = DbUserUtils.get_user_profile(user_name)
        return jsonify(res), 200
    except(NotFound) as e:
        return jsonify(e.body), e.status_code

@user.route('/change_password/<user_name>', methods=['PUT'])
def change_password(user_name):
    try:
        request_body = json.loads(request.get_data())
        DbUserUtils.update_password(user_name, request_body)
        return jsonify({}), 204
    except (BadRequest, NotFound, ValidationFailed) as e:
        return jsonify(e.body), e.status_code

@user.route('/update_profile/<user_name>', methods=['POST'])
def update_profile(user_name):
    try:
        request_body = json.loads(request.get_data())
        DbUserUtils.update_profile(user_name, request_body)
        return jsonify(DbUserUtils.get_user_profile(user_name)), 201
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

@user.route('/get_user_cals/<user_name>', methods=['GET'])
def get_cals(user_name):
    try:
        res = DbUserUtils.get_all_cals(user_name)
        return jsonify(res), 200
    except (NotFound) as e:
        return jsonify(e.body), e.status_code

'''The following route deals with subscribers'''
@user.route('/newSubscriber', methods=['POST'])
def create_subscriber():
    try:
        request_body = json.loads(request.get_data())
        DbUserUtils.add_to_Subscriber_List(request_body)
        return jsonify({}), 201
    except(BadRequest, ValidationFailed) as e:
        return jsonify(e.body), e.status_code
