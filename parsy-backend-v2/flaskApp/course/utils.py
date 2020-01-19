import sys
from flaskApp import db
#from flaskApp.course.reportbot import minibot
from flaskApp.models import Calendar, User, Courseitem, HelpSession, Exam, ClassMeeting, Assignment, Report, Slot
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getOHData, getExamData, getClassMeetingData, getAssignmentData
import string
import copy
import uuid
import time


'''Special method called in User to duplicate contents of one cal to another'''
def duplicateCal(userid, cal_id):
    cal = Calendar.query.filter_by(calID=cal_id).first()
    #caluuid = str(uuid.uuid4)
    print("USER!!!")
    print(userid)
    calendaruuid = str(uuid.uuid4())
    duplical = Calendar(calID=calendaruuid, user=userid)
    print((duplical).calID)
    db.session.add(duplical)

    duplical_id = duplical.calID
    print(duplical_id)

    courses = Courseitem.query.filter_by(calender=cal_id).all()
    for course in courses:
        course_id = course.courseuuid
        duplicourse = Courseitem(courseID=course.courseID, calender=duplical_id, courseName=course.courseName, professor=course.professor)
        db.session.add(duplicourse)
        db.session.flush()
        duplicourse_id = duplicourse.courseuuid

        help_sessions = HelpSession.query.filter_by(course=course_id).all()
        assignments = Assignment.query.filter_by(course=course_id).all()
        exams = Exam.query.filter_by(course=course_id).all()
        class_meetings = ClassMeeting.query.filter_by(course=course_id).all()

        for help in help_sessions:
            duplihelp = HelpSession(course=duplicourse_id, type=help.type, times=help.times, location=help.location)
            db.session.add(duplihelp)
        for exam in exams:
            dupliexam = Exam(course=duplicourse_id, type=exam.type, datetime=exam.datetime, location=exam.location)
            db.session.add(dupliexam)
        for assignment in assignments:
            dupliassignment = Assignment(course=duplicourse_id, type=assignment.type, datetime=assignment.datetime, location=assignment.location)
            db.session.add(dupliassignment)
        for meeting in class_meetings:
            duplimeeting = HelpSession(course=duplicourse_id, type=meeting.type, times=meeting.times, location=meeting.location)
            db.session.add(duplimeeting)

    db.session.commit()
    return duplical_id


'''Below Methods are for checking if items exist in DB'''
def check_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise NotFound

def check_cal(cal_id):
    cal = Calendar.query.filter_by(calID=cal_id).first()
    if cal is None:
        raise NotFound
    return cal

def check_course(cal_ID, course_ID):
    help = Courseitem.query.filter_by(courseID=course_ID, calender=cal_ID).first()
    if help is None:
        raise NotFound
    return help

def check_contains_course(cal_ID, course_Name):
    help = Courseitem.query.filter_by(calender=cal_ID, courseName=course_Name).first()
    if help is not None:
        raise ValidationFailed

def getCourseInfo(courseid):
    course = Courseitem.query.filter_by(courseuuid=courseid).first()
    res = _asdict(course)

    times = Slot.query.filter_by(course=courseid, type='support').all()
    exams = Slot.query.filter_by(course=courseid, type='exams').all()
    classMeetings = Slot.query.filter_by(course=courseid, type='meetings').all()
    assignments = Slot.query.filter_by(course=courseid, type='assignments').all()

    res['support'] = [_asdict(time) for time in times]
    res['exam'] = [_asdict(exam) for exam in exams]
    res['class_meeting'] = [_asdict(meeting) for meeting in classMeetings]
    res['assignment'] = [_asdict(assignment) for assignment in assignments]
    return res

'''This exists
for restoring the customized cal'''
def getOriginalContent(content):
    print("CONTENT HERE")
    print(content)
    res = copy.deepcopy(content)
    for course in res:
        courseID = course['courseID']
        res_OH = getOHData(courseID)
        res_exam = getExamData(courseID)
        res_assignment = getAssignmentData(courseID)
        res_meeting = getClassMeetingData(courseID)

        supports = []
        exams = []
        classMeetings = []
        assignments = []
        for oh in res_OH['support']:
            times = oh['times'].split(",")
            for time in times:
                fixed_time = time.lstrip()
                dict = {"location" : oh['location'], "type" : oh['type'], "times" : fixed_time, "course" : course['courseuuid']}
                for item in course['support']:
                    if oh['location'] in item.values() and oh['type'] in item.values() and fixed_time in item.values():
                        dict['helpSessionId'] = item['helpSessionId']
                        break
                supports.append(dict)
        for exam in res_exam['exams']:
            dict = {"location" : exam['location'], "type" : exam['type'], "datetime" : exam['datetime'], "course" : course['courseuuid']}
            for item in course['exam']:
                if exam['location'] in item.values() and exam['type'] in item.values() and exam['datetime'] in item.values():
                    dict['examId'] = item['examId']
                    break
            exams.append(dict)
        for assignment in res_assignment['assignments']:
            dict = {"location" : assignment['location'], "type" : assignment['type'], "datetime" : assignment['datetime'], "course" : course['courseuuid']}
            for item in course['assignment']:
                if assignment['location'] in item.values() and assignment['type'] in item.values() and assignment['datetime'] in item.values():
                    dict['assignmentId'] = item['assignmentId']
                    break
            assignments.append(dict)
        for meeting in res_meeting['meetings']:
            dict = {"location" : meeting['location'], "type" : meeting['type'], "times" : meeting['times'], "course" : course['courseuuid']}
            for item in course['class_meeting']:
                if meeting['location'] in item.values() and meeting['type'] in item.values() and  meeting['times'] in item.values():
                    dict['classmeetingId'] = item['classmeetingId']
                    break
            classMeetings.append(dict)

        course['support'] = supports
        course['exam'] = exams
        course['class_meeting'] = classMeetings
        course['assignment'] = assignments
    return res


'''End of validity checking helper methods'''

class DbCourseitemUtils(object):

    def creatCal(request_body):
        if 'username' not in request_body:
            raise BadRequest
        username = request_body['username']
        check_user(username)
        caluuid = str(uuid.uuid4())
        calendar = Calendar(calID=caluuid, user=username, school_id=1)
        db.session.add(calendar)
        id = calendar.calID
        db.session.commit()
        return id

    def get_cal(cal_id):
        cal = check_cal(cal_id)
        res = _asdict(cal)
        courses = Courseitem.query.filter_by(calender=cal_id).all()
        res['content'] = [_asdict(course) for course in courses]
        for course in res['content']:
            times = Slot.query.filter_by(course=course['courseuuid'], type='support').all()
            exams = Slot.query.filter_by(course=course['courseuuid'], type='exams').all()
            assignments = Slot.query.filter_by(course=course['courseuuid'], type='assignments').all()
            classMeetings = Slot.query.filter_by(course=course['courseuuid'], type='meetings').all()
            course['support'] = [_asdict(time) for time in times]
            course['exam'] = [_asdict(exam) for exam in exams]
            course['class_meeting'] = [_asdict(meeting) for meeting in classMeetings]
            course['assignment'] = [_asdict(assignment) for assignment in assignments]
        #res['originalContent'] = getOriginalContent(res['content'])
        return res

    def delete_cal(cal_id):
        cal = check_cal(cal_id)
        courses = Courseitem.query.filter_by(calender=cal_id).all()
        for course in courses:
            course_id = course.courseuuid
            times = Slot.query.filter_by(course=course_id, type='support').all()
            exams = Slot.query.filter_by(course=course_id, type='exams').all()
            meetings = Slot.query.filter_by(course=course_id, type='meetings').all()
            assignments = Slot.query.filter_by(course=course_id, type='assignments').all()
            for time in times:
                db.session.delete(time)
            for exam in exams:
                db.session.delete(exam)
            for meeting in meetings:
                db.session.delete(meeting)
            for assignment in assignments:
                db.session.delete(assignment)
            Courseitem.query.filter_by(courseuuid=course_id).delete()
        Calendar.query.filter_by(calID=cal_id).delete()
        db.session.commit()

    def delete_classHelpTimes(cal_ID, course_ID):
        cal = check_cal(cal_ID)
        course = check_course(cal_ID, course_ID)
        specific_course_id = course.courseuuid
        times = Slot.query.filter_by(course=specific_course_id, type='support').all()
        exams = Slot.query.filter_by(course=specific_course_id, type='exams').all()
        meetings = Slot.query.filter_by(course=specific_course_id, type='meetings').all()
        assignments = Slot.query.filter_by(course=specific_course_id, type='assignments').all()
        for time in times:
            db.session.delete(time)
        for exam in exams:
            db.session.delete(exam)
        for meeting in meetings:
            db.session.delete(meeting)
        for assignment in assignments:
            db.session.delete(assignment)
        Courseitem.query.filter_by(courseID=course_ID, calender=cal_ID).delete()
        db.session.commit()

    def add_helpTime(cal_ID, courseID):
        cal = check_cal(cal_ID)
        
        res_OH = getOHData(courseID)
        res_exam = getExamData(courseID)
        res_assignment = getAssignmentData(courseID)
        res_meeting = getClassMeetingData(courseID)

        course_Name = res_OH['name']
        check_contains_course(cal_ID, course_Name)
        course = Courseitem(courseID=res_OH['id'], courseName=res_OH['name'], calender=cal_ID, professor=res_OH['prof'])
        print('got course')
        db.session.add(course)
        db.session.flush()
        courseid = course.courseuuid
        db.session.commit()
        for course in res_OH['support']:
            times = course['times'].split(",")
            for time in times:
                fixed_time = time.lstrip()
                help = Slot(course=courseid, type='support', sub_type=course['type'], is_weekly=True, time=fixed_time, location=course['location'])
                db.session.add(help)
        for exam in res_exam['exams']:
            exam = Slot(course=courseid, type='exams', sub_type=exam['type'], is_weekly=False, time=exam['datetime'], location=exam['location'])
            db.session.add(exam)
        for assignment in res_assignment['assignments']:
            assignment = Slot(course=courseid, type='assignments', sub_type=assignment['type'], is_weekly=False, time=assignment['datetime'], location=assignment['location'])
            db.session.add(assignment)
        for meeting in res_meeting['meetings']:
            classMeeting = Slot(course=courseid, type='meetings', sub_type=meeting['type'], is_weekly=True, time=meeting['times'], location=meeting['location'])
            db.session.add(classMeeting)
        db.session.commit()
        res = getCourseInfo(courseid)
        return res

    def add_new_data_to_db(request_body):
        #time.sleep(2)
        print(request_body)
        if 'courseID' not in request_body or 'course_link' not in request_body or 'submit_method' not in request_body:
            raise BadRequest
        if not request_body['courseID'] or not request_body['course_link'] or not request_body['submit_method']:
            raise BadRequest
        if request_body['submit_method'] != 'url' and request_body['submit_method'] != 'pdf':
            raise BadRequest
        report = Report(courseID=request_body['courseID'], semester="Fall 2019", url=request_body['course_link'])
        db.session.add(report)
        db.session.commit()
        courseID = request_body['courseID'].strip().upper()
        url = request_body['course_link']

        '''Check if courseID in course db and return NotFound if not'''
        query = " select distinct CNum from course where CNum \
        = '%s' and Semester = 'Fall 2019';" % (courseID)
        sql = text(query)
        resTuple = db.engine.execute(sql)
        if resTuple.rowcount == 0:
            raise NotFound

        '''Check if url is valid part of jhu domain, return ValidationFailed'''
        if not url.startswith("jhu.edu") and '.jhu.edu' not in url and '/jhu.edu' not in url:
            raise ValidationFailed

        '''Plan: 1) check if courseID in course db and return NotFound if not
            2) Check if url is valid part of jhu domain, return ValidationFailed (DONE) if not
            3) Run Web bot
            4) Insert results into db
            5) Insert url/success/failure into table (DONE)
        '''
        #minibot.main(url, url, courseID)
        report.status = "success"
        db.session.commit()
