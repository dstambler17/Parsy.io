import sys
from flaskApp import db
from flaskApp.models import HelpSession, Courseitem, Calendar
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getOHData
import string

def check_here_cal(cal_Id):
    cal = Calendar.query.filter_by(calID=cal_Id).first()
    if cal is None:
        print("ERROR IN check_here_cal")
        raise NotFound
    return cal

def check_here_course(cal_Id, course_ID):
    course = Courseitem.query.filter_by(courseID=course_ID, calender=cal_Id).first()
    if course is None:
        print("ERROR IN check_here_course")
        raise NotFound
    return course

def check_OH_time_slot(timeslot_id):
    timeslot = HelpSession.query.filter_by(helpSessionId=timeslot_id).first()
    if timeslot is None:
        print("ERROR IN check_oh_slot")
        raise NotFound
    return timeslot

'''This method exists due to some
problem with implementation on frontend'''
def check_OH_time_slot_del(time, location, type, course):
    timeslot = HelpSession.query.filter_by(type=type, times=time, location=location, course=course).first()
    if timeslot is None:
        print("check IN check_oh_slot_del")
        return False
    return timeslot

def delete_all_OH(course_uuid):
    office_hours = HelpSession.query.filter_by(course=course_uuid).all()
    for office_hour in office_hours:
        db.session.delete(office_hour)
    db.session.commit()

'''The following methods are for adding office hours
    this makes it much more customizable on the client side'''
def check_contains_OH(type, course, time, location):
    help = HelpSession.query.filter_by(course=course, type=type, times=time, location=location).first()
    if help is not None:
        raise ValidationFailed

def add_all_OH(course_id, course_uuid):
    data = getOHData(course_id)
    support = data['support']
    for item in support:
        type = item["type"]
        times = item["times"].split(",")
        location = item["location"]
        for time in times:
            office_hour_time = time.lstrip()
            check_contains_OH(type, course_uuid, office_hour_time, location)
            help = HelpSession(course=course_uuid, type=type, times=office_hour_time, location=location)
            db.session.add(help)
        db.session.commit()

def add_OH_based_on_type(course_id, course_uuid, oh_type):
    data = getOHData(course_id)
    support = data['support']
    for item in support:
        type = item["type"]
        times = item["times"].split(",")
        location = item["location"]
        if oh_type in type:
            for time in times:
                office_hour_time = time.lstrip()
                helpCheck = HelpSession.query.filter_by(course=course_uuid, type=type, times=office_hour_time, location=location).first()
                if helpCheck is None:
                    help = HelpSession(course=course_uuid, type=type, times=office_hour_time, location=location)
                    db.session.add(help)
            db.session.commit()

def validate_oh_input(course_name, course_uuid, content, support):
    supportList = []
    for x in support:
        type = x["type"]
        times = x["times"].split(",")
        location = x["location"]
        for time in times:
            office_hour_time = time.lstrip()
            dictItem = {"time": office_hour_time, "location" : location, "type": type}
            supportList.append(dictItem)
    for item in content:
        if item not in supportList:
            print("THIS ITEM NOT IN SUP LIST")
            print(item)
            print("CONTENT")
            print(content)
            print("BELOW IS supportList")
            print(supportList)
            raise ValidationFailed


class DbHelpSessionUtils(object):
    def add_OH_slot(calID, courseID, request_body):
        CATAGORIES = ['Prof', 'TA'] #Add more here
        check_here_cal(calID)
        course = check_here_course(calID, courseID)
        course_name = course.courseName
        courseID = course.courseID
        course_uuid = course.courseuuid
        if 'content' not in request_body or 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            add_all_OH(courseID, course_uuid)
        elif request_body['all'] in CATAGORIES:
            add_OH_based_on_type(courseID, course_uuid, request_body['all'])
        else:
            data = getOHData(courseID)
            in_db_office_hours = data['support']
            content = request_body['content']
            validate_oh_input(courseID, course_uuid, content, in_db_office_hours)
            for item in content:
                check_contains_OH(item['type'], course_uuid, item['time'], item['location'])
                help = HelpSession(course=course_uuid, type=item['type'], times=item['time'], location=item['location'])
                db.session.add(help)
            db.session.commit()

    def delete_OH_slot(calID, courseID, request_body):
        check_here_cal(calID)
        course = check_here_course(calID, courseID)
        course_uuid = course.courseuuid
        if 'content' not in request_body and 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            delete_all_OH(course_uuid)
        else:
            content = request_body['content']
            for item in content:
                office_hour = check_OH_time_slot_del(item['time'], item['location'], item['type'], course_uuid)
                if office_hour is not False:
                    db.session.delete(office_hour)
            db.session.commit()

    def get_OH_slot_details(calID, courseID, office_hour):
        check_here_cal(calID)
        check_here_course(calID, courseID)
        office_hour = check_OH_time_slot(office_hour)
        res = _asdict(office_hour)
        return res

    def restore_all_original_OH(calID, courseID):
        check_here_cal(calID)
        course = check_here_course(calID, courseID)
        #course_name = course.courseName
        course_uuid = course.courseuuid
        delete_all_OH(course_uuid)
        add_all_OH(courseID, course_uuid)
