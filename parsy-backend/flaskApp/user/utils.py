import sys
from flaskApp import db, bcrypt
import json
from flaskApp.models import User, Calendar, EmailSubscriber
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict
import string
from google.oauth2 import id_token
from google.auth.transport import requests
from apiclient import discovery
import httplib2
from oauth2client import client
from flaskApp.course.utils import duplicateCal

def check_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise NotFound
    return user

def check_contains_user(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        raise ValidationFailed

def extract_extra_profile_info(request_body):
    info = {}
    if 'first_name' in request_body:
        info['first_name'] = request_body['first_name']
    if 'last_name' in request_body:
        info['last_name'] = request_body['last_name']
    if 'major' in request_body:
        info['major'] = request_body['major']
    if 'school' in request_body:
        info['school'] = request_body['school']
    if 'email' in request_body:
        info['email'] = request_body['email']
    return info

class DbUserUtils(object):
    def update_profile(username, request_body):
        user = check_user(username)
        profile = extract_extra_profile_info(request_body)
        for k,v in profile.items():
            setattr(user, k, v)
        db.session.commit()

    def SignIn_user_gauth(request_body):
        print(request_body)
        if 'creds' not in request_body or 'calid' not in request_body:
            raise BadRequest
        print("MADE IT")
        CLIENT_SECRET_PATH = 'flaskApp/user/client_secret_528707814554-sahtu1f07gvbs8sksjol3dgmjcg45h1e.apps.googleusercontent.com.json'
        auth_code = request_body['creds']
        cal_id = request_body['calid']
        # Specify the CLIENT_ID of the app that accesses the backend
        CLIENT_ID = '528707814554-sahtu1f07gvbs8sksjol3dgmjcg45h1e.apps.googleusercontent.com'
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_PATH,
            ['https://www.googleapis.com/auth/calendar.events', 'profile', 'email'],
            auth_code)
        id_token = credentials.id_token
        print(id_token)
        print(credentials)
        #print(json.dumps(credentials, default = myconverter))
        #idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        if id_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValidationFailed
        userid = id_token['sub']
        first_name = id_token['given_name']
        last_name = id_token['family_name']
        email = id_token['email']

        #http_auth = credentials.authorize(httplib2.Http())
        #service = discovery.build('calendar', 'v3', credentials=credentials)

        #check if userid is in db as username
        print(userid)
        user = User.query.filter_by(username=userid[0:20]).first() #last char is extra for some reason
        if user is None:
            #NOTE TO Self, REMOVE password field from DB
            user = User(username=userid, affiliation='student', first_name=first_name, last_name=last_name, email=email, creds=credentials.to_json())
            db.session.add(user)
            db.session.commit()
            new_cal_id = duplicateCal(userid, cal_id)
            return {'calId' : str(new_cal_id), 'id_token' : id_token}
        else:
            print(userid)
            cal = Calendar.query.filter_by(user=userid[0:20]).first()
            return {'calId' : str(cal.calID), 'id_token' : id_token}

    def SignIn_user_gauth_already_signedIn(request_body):
        print(request_body)
        if 'userid' not in request_body or 'calid' not in request_body:
            raise BadRequest
        cal_id = request_body['calid']
        userid = request_body['userid']
        print(userid)

        #check if userid is in db as username
        print(userid)
        user = User.query.filter_by(username=userid[0:20]).first() #last char is extra for some reason
        #NOTE: THIS should not happen
        if user is None:
            #NOTE TO Self, REMOVE password field from DB
            user = User(username=userid, affiliation='student', first_name=first_name, last_name=last_name, email=email)
            db.session.add(user)
            db.session.commit()
            new_cal_id = duplicateCal(userid, cal_id)
            return {'calId' : str(new_cal_id)}
        else:
            cal = Calendar.query.filter_by(user=userid[0:20]).first()
            return {'calId' : str(cal.calID)}



    def add_new_user(request_body):
        if 'username' not in request_body or 'password' not in request_body or 'affiliation' not in request_body:
            raise BadRequest
        '''Checks that username doesn't already exist'''
        username = request_body['username']
        check_contains_user(username)
        '''Checks for proper affiliation'''
        affiliation = request_body['affiliation']
        if affiliation != 'student' and affiliation != 'instructor' and affiliation != 'admin':
            print('spelling')
            raise ValidationFailed
        '''Deals with password'''
        unencrypted_password = request_body.get('password', '')
        password = bcrypt.generate_password_hash(unencrypted_password).decode('utf-8')
        user = User(username=username, password=password, affiliation=affiliation)
        db.session.add(user)
        db.session.commit()
        DbUserUtils.update_profile(username, request_body)

    def update_password(username, request_body):
        user = check_user(username)
        if 'password' not in request_body or 'new_password' not in request_body:
            raise BadRequest
        new_password = request_body['new_password']
        password = request_body['password']
        if not bcrypt.check_password_hash(user.password, password):
            raise ValidationFailed
        new_password_encrypt = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = new_password_encrypt
        db.session.commit()
        #bcrypt.generate_password_hash(password).decode('utf-8')

    def user_login(request_body):
        username = request_body.get('username', '')
        password = request_body.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user is None or not bcrypt.check_password_hash(user.password, password):
            raise ValidationFailed

    def get_user_profile(username):
        user = check_user(username)
        res = _asdict(user)
        res.pop('password', None)
        return res

    def get_all_cals(username):
        user = check_user(username)
        cals = Calendar.query.filter_by(user=username).all()
        res = [_asdict(cal) for cal in cals]
        res = sorted(res, key=lambda x: x['date'], reverse=True)
        return res

    '''Helper for endpoint in the landing page'''
    def add_to_Subscriber_List(request_body):
        if 'name' not in request_body or 'email' not in request_body:
            raise BadRequest
        if '@' not in request_body['email']:
            raise ValidationFailed
        if len(request_body['name']) < 1:
            raise ValidationFailed
        emailSub = EmailSubscriber.query.filter_by(email=request_body['email']).first()
        if emailSub is not None:
            raise BadRequest
        new_email_sub = EmailSubscriber(name=request_body['name'], email=request_body['email'])
        db.session.add(new_email_sub)
        db.session.commit()
