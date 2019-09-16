import sys
from flaskApp import db
from flaskApp.models import Assignment, Courseitem, Calendar
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getAssignmentData
import string

def check_cal(cal_Id):
    cal = Calendar.query.filter_by(calID=cal_Id).first()
    if cal is None:
        raise NotFound
    return cal

def check_course(cal_Id, course_ID):
    course = Courseitem.query.filter_by(courseID=course_ID, calender=cal_Id).first()
    if course is None:
        raise NotFound
    return course

def check_assignment_time_slot(timeslot_id):
    timeslot = Assignment.query.filter_by(assignmentId=timeslot_id).first()
    if timeslot is None:
        raise NotFound
    return timeslot

def check_assignment_time_slot_del(datetime, location, type, course_uuid):
    timeslot = Assignment.query.filter_by(datetime=datetime, location=location, type=type, course=course_uuid).first()
    if timeslot is None:
        return False
    return timeslot

def check_contains_assignment(type, course, datetime, location):
    assignment = Assignment.query.filter_by(course=course, type=type, datetime=datetime, location=location).first()
    if assignment is not None:
        raise ValidationFailed

'''Methods for adding Assignments'''
def add_all_assignments(courseID, course_uuid):
    res = {"added" : []}
    data = getAssignmentData(courseID)
    assignments = data['assignments']
    for item in assignments:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        check_contains_assignment(type, course_uuid, time, location)
        assignment = Assignment(course=course_uuid, type=type, datetime=time, location=location)
        res["added"].append(_asdict(assignment))
        db.session.add(assignment)
    db.session.commit()
    return res

def add_assignment_based_on_type(courseID, course_uuid, assignment_type):
    res = {"added" : []}
    data = getAssignmentData(courseID)
    assignments = data['assignments']
    for item in assignments:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        if assignment_type in type:
            assignment_check = Assignment.query.filter_by(course=course_uuid, type=type, datetime=time, location=location).first()
            if assignment_check is None:
                assignment = Assignment(course=course_uuid, type=type, datetime=time, location=location)
                db.session.add(assignment)
                res["added"].append(_asdict(assignment))
    db.session.commit()
    return res

def validate_assignment_input(courseID, course_uuid, content, assignments):
    assignmentList = []
    for item in assignments:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        dictItem = {"datetime": time, "location" : location, "type": type}
        assignmentList.append(dictItem)
    for assignment in content:
        if assignment not in assignmentList:
            raise ValidationFailed

def delete_all_assignments(course_uuid):
    assignments = Assignment.query.filter_by(course=course_uuid).all()
    for assignment in assignments:
        db.session.delete(assignment)
    db.session.commit()

class DbAssignmentUtils(object):
    def get_assignment_slot_details(calID, courseID, assignment):
        check_cal(calID)
        check_course(calID, courseID)
        assignmentSlot = check_assignment_time_slot(assignment)
        res = _asdict(assignmentSlot)
        return res

    def add_Assignment_slot(calID, courseID, request_body):
        CATAGORIES = ['Homework'] #Add more here
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID_sem = course.courseID
        course_uuid = course.courseuuid
        if 'content' not in request_body or 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            res = add_all_assignments(course_ID_sem, course_uuid)
            return res
        elif request_body['all'] in CATAGORIES:
            res = add_assignment_based_on_type(course_ID_sem, course_uuid, request_body['all'])
            return res
        else:
            res = {"added" : []}
            data = getAssignmentData(course_ID_sem)
            in_db_assignments = data['assignments']
            content = request_body['content']
            validate_assignment_input(course_ID_sem, course_uuid, content, in_db_assignments)
            for item in content:
                check_contains_assignment(item['type'], course_uuid, item['datetime'], item['location'])
                assignment = Assignment(course=course_uuid, type=item['type'], datetime=item['datetime'], location=item['location'])
                db.session.add(assignment)
                res["added"].append(_asdict(assignment))
            db.session.commit()
            return res

    def delete_assignment_slot(calID, courseID, request_body):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_uuid = course.courseuuid
        if 'content' not in request_body and 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            delete_all_assignments(course_uuid)
        else:
            content = request_body['content']
            for item in content:
                assignment = check_assignment_time_slot_del(item['time'], item['location'], item['type'], course_uuid)
                if assignment is not False:
                    db.session.delete(assignment)
            db.session.commit()

    def restore_all_original_assignment(calID, courseID):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID = course.courseID
        course_uuid = course.courseuuid
        delete_all_assignments(course_uuid)
        add_all_assignments(course_ID, course_uuid)
