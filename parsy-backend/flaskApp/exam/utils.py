import sys
from flaskApp import db
from flaskApp.models import Exam, Courseitem, Calendar
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getExamData
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

def check_exam_time_slot(timeslot_id):
    timeslot = Exam.query.filter_by(examId=timeslot_id).first()
    if timeslot is None:
        raise NotFound
    return timeslot

def check_exam_time_slot_del(datetime, location, type, course_uuid):
    timeslot = Exam.query.filter_by(datetime=datetime, location=location, type=type, course=course_uuid).first()
    if timeslot is None:
        return False
    return timeslot

def check_contains_exam(type, course, datetime, location):
    help = Exam.query.filter_by(course=course, type=type, datetime=datetime, location=location).first()
    if help is not None:
        raise ValidationFailed

'''Methods for adding Exams'''
def add_all_exams(courseID, course_uuid):
    res = {"added" : []}
    data = getExamData(courseID)
    exams = data['exams']
    for item in exams:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        check_contains_exam(type, course_uuid, time, location)
        exam = Exam(course=course_uuid, type=type, datetime=time, location=location)
        res["added"].append(_asdict(exam))
        db.session.add(exam)
    db.session.commit()
    return res

def add_exam_based_on_type(courseID, course_uuid, exam_type):
    res = {"added" : []}
    data = getExamData(courseID)
    exams = data['exams']
    for item in exams:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        if exam_type in type:
            exam_check = Exam.query.filter_by(course=course_uuid, type=type, datetime=time, location=location).first()
            if exam_check is None:
                exam = Exam(course=course_uuid, type=type, datetime=time, location=location)
                db.session.add(exam)
                res["added"].append(_asdict(exam))
    db.session.commit()
    return res

def validate_exam_input(courseID, course_uuid, content, exams):
    examList = []
    for item in exams:
        type = item["type"]
        time = item["datetime"]
        location = item["location"]
        dictItem = {"datetime": time, "location" : location, "type": type}
        examList.append(dictItem)
    for exam in content:
        if exam not in examList:
            raise ValidationFailed

def delete_all_exams(course_uuid):
    exams = Exam.query.filter_by(course=course_uuid).all()
    for exam in exams:
        db.session.delete(exam)
    db.session.commit()

class DbExamUtils(object):
    def get_exam_slot_details(calID, courseID, exam):
        check_cal(calID)
        check_course(calID, courseID)
        examSlot = check_exam_time_slot(exam)
        res = _asdict(examSlot)
        return res

    def add_Exam_slot(calID, courseID, request_body):
        CATAGORIES = ['Midterm', 'Final', 'Quiz'] #Add more here
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID_sem = course.courseID
        course_uuid = course.courseuuid
        if 'content' not in request_body or 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            res = add_all_exams(course_ID_sem, course_uuid)
            return res
        elif request_body['all'] in CATAGORIES:
            res = add_exam_based_on_type(course_ID_sem, course_uuid, request_body['all'])
            return res
        else:
            res = {"added" : []}
            data = getExamData(course_ID_sem)
            in_db_exams = data['exams']
            content = request_body['content']
            validate_exam_input(course_ID_sem, course_uuid, content, in_db_exams)
            for item in content:
                check_contains_exam(item['type'], course_uuid, item['datetime'], item['location'])
                exam = Exam(course=course_uuid, type=item['type'], datetime=item['datetime'], location=item['location'])
                db.session.add(exam)
                res["added"].append(_asdict(exam))
            db.session.commit()
            return res

    def delete_exam_slot(calID, courseID, request_body):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_uuid = course.courseuuid
        if 'content' not in request_body and 'all' not in request_body:
            raise BadRequest
        if request_body['all'] == 'yes':
            delete_all_exams(course_uuid)
        else:
            content = request_body['content']
            for item in content:
                exam = check_exam_time_slot_del(item['time'], item['location'], item['type'], course_uuid)
                if exam is not False:
                    db.session.delete(exam)
            db.session.commit()

    def restore_all_original_exam(calID, courseID):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID = course.courseID
        course_uuid = course.courseuuid
        delete_all_exams(course_uuid)
        add_all_exams(course_ID, course_uuid)
