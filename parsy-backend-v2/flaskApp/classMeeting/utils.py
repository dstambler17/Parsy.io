import sys
from flaskApp import db
from flaskApp.models import ClassMeeting, Courseitem, Calendar
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getClassMeetingData
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

def check_classMeeting_time_slot(timeslot_id):
    classMeeting = ClassMeeting.query.filter_by(classmeetingId=timeslot_id).first()
    if classMeeting is None:
        raise NotFound
    return classMeeting

def check_classMeeting_time_slot_del(time, location, type, course_uuid):
    classMeeting = ClassMeeting.query.filter_by(times=time, location=location, type=type, course=course_uuid).first()
    if classMeeting is None:
        return False
    return classMeeting

def check_contains_classMeeting(type, course, times, location):
    classMeeting = ClassMeeting.query.filter_by(course=course, type=type, times=times, location=location).first()
    if classMeeting is not None:
        raise ValidationFailed

'''Methods for adding adding and removing class meeting times'''
def add_all_classMeetings(courseID, course_uuid):
    res = {"added" : []}
    data = getClassMeetingData(courseID)
    meetings = data['meetings']
    for item in meetings:
        type = item["type"]
        time = item["times"]
        location = item["location"]
        check_contains_classMeeting(type, course_uuid, time, location)
        meeting = ClassMeeting(course=course_uuid, type=type, times=time, location=location)
        res["added"].append(_asdict(meeting))
        db.session.add(meeting)
    db.session.commit()
    return res

def add_classMeeting_based_on_type(courseID, course_uuid, classMeeting_type):
    res = {"added" : []}
    data = getClassMeetingData(courseID)
    meetings = data['meetings']
    for item in meetings:
        type = item["type"]
        time = item["times"]
        location = item["location"]
        if classMeeting_type in type:
            meeting_check = ClassMeeting.query.filter_by(course=course_uuid, type=type, times=time, location=location).first()
            if meeting_check is None:
                meeting = ClassMeeting(course=course_uuid, type=type, times=time, location=location)
                db.session.add(meeting)
                res["added"].append(_asdict(meeting))
    db.session.commit()
    return res

def validate_classMeeting_input(courseID, course_uuid, content, classMeetings):
    classMeetingList = []
    for item in classMeetings:
        type = item["type"]
        time = item["times"]
        location = item["location"]
        dictItem = {"times": time, "location" : location, "type": type}
        classMeetingList.append(dictItem)
    for meeting in content:
        if meeting not in classMeetingList:
            raise ValidationFailed

def delete_all_classMeetings(course_uuid):
    classMeetings = ClassMeeting.query.filter_by(course=course_uuid).all()
    for classMeeting in classMeetings:
        db.session.delete(classMeeting)
    db.session.commit()

class DbClassMeetingUtils(object):
    def get_class_meeting_slot_details(calID, courseID, meeting_time):
        check_cal(calID)
        check_course(calID, courseID)
        classMeetingSlot = check_classMeeting_time_slot(meeting_time)
        res = _asdict(classMeetingSlot)
        return res

    def add_class_meeting_slot(calID, courseID, request_body):
        CATAGORIES = ['Lecture', 'Section', 'Lab'] #Add more here
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID_sem = course.courseID
        course_uuid = course.courseuuid
        if 'content' not in request_body or 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            res = add_all_classMeetings(course_ID_sem, course_uuid)
            return res
        elif request_body['all'] in CATAGORIES:
            res = add_classMeeting_based_on_type(course_ID_sem, course_uuid, request_body['all'])
            return res
        else:
            res = {"added" : []}
            data = getClassMeetingData(course_ID_sem)
            in_db_meetings = data['meetings']
            content = request_body['content']
            validate_classMeeting_input(course_ID_sem, course_uuid, content, in_db_meetings)
            for item in content:
                check_contains_classMeeting(item['type'], course_uuid, item['times'], item['location'])
                classMeeting = ClassMeeting(course=course_uuid, type=item['type'], times=item['times'], location=item['location'])
                db.session.add(classMeeting)
                res["added"].append(_asdict(classMeeting))
            db.session.commit()
            return res

    def delete_class_meeting_slot(calID, courseID, request_body):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_uuid = course.courseuuid
        if 'content' not in request_body and 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            delete_all_classMeetings(course_uuid)
        else:
            content = request_body['content']
            for item in content:
                classMeeting = check_classMeeting_time_slot_del(item['time'], item['location'], item['type'], course_uuid)
                if classMeeting is not False:
                    db.session.delete(classMeeting)
            db.session.commit()

    def restore_all_original_class_meeting(calID, courseID):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID = course.courseID
        course_uuid = course.courseuuid
        delete_all_classMeetings(course_uuid)
        add_all_classMeetings(course_ID, course_uuid)
