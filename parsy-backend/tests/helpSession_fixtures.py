import pytest
import uuid
from flaskApp.models import *

@pytest.fixture
def create_cal_course(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    courseid = course.courseuuid
    courseIDSem = course.courseID

    def _delete_cal_course():
        courseSlot = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(courseSlot)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course)
    return id, courseIDSem

@pytest.fixture
def create_cal_course_helpSession(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    courseid = course.courseuuid
    helpCourseitem = course.courseID

    helpses = HelpSession(course=courseid, type="Professor Office Hours", times="Thursday 3:00pm-4:30pm", location="Malone 227")
    db.session.add(helpses)
    db.session.commit()
    helpsesId = helpses.helpSessionId


    def _delete_cal_course_helpSession():
        helpses = HelpSession.query.filter_by(helpSessionId=helpsesId).first()
        db.session.delete(helpses)
        db.session.commit()

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_helpSession)
    return id, helpCourseitem, helpsesId

@pytest.fixture
def create_cal(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    def _delete_cal():
        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal)
    return id

@pytest.fixture
def create_cal_course_helpSession_del(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    course_uuid = course.courseuuid
    coursesSemId = course.courseID

    helpses = HelpSession(course=course_uuid, type="Professor Office Hours", times="Thursday 3:00pm-4:30pm", location="Malone 227")
    db.session.add(helpses)
    db.session.commit()
    helpsesId = helpses.helpSessionId

    def _delete_cal_course_helpSession_del():
        course = Courseitem.query.filter_by(courseuuid=course_uuid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_helpSession_del)
    return id, coursesSemId, helpsesId


@pytest.fixture
def create_cal_course_helpSession_del_all(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    courseid = course.courseuuid
    courseIDSem = course.courseID

    helpses = HelpSession(course=courseid, type="Professor Office Hours", times="Thursday 3:00pm-4:30pm", location="Malone 227")
    helpsesTwo = HelpSession(course=courseid, type="TA Office Hours", times="Friday 3:00pm-4:30pm", location="Malone 122")
    db.session.add(helpses)
    db.session.add(helpsesTwo)
    db.session.commit()
    helpsesId = helpses.helpSessionId

    def _delete_cal_course_helpSession_del_all():

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_helpSession_del_all)
    return id, courseIDSem, helpsesId

@pytest.fixture
def delete_helpSess(request, db):
    def _delete_helpSession():
        help = HelpSession.query.filter_by(type="Professor Office Hours").first()
        db.session.delete(help)
        db.session.commit()

    request.addfinalizer(_delete_helpSession)
    return

@pytest.fixture
def delete_helpSess_all(request, db):
    def _delete_helpSession():
        help = HelpSession.query.filter_by(type="TA Office Hours").all()
        for item in help:
            db.session.delete(item)
        db.session.commit()
        help_two = HelpSession.query.filter_by(type="Professor Office Hours").all()
        for itemtwo in help_two:
            db.session.delete(itemtwo)
        db.session.commit()

    request.addfinalizer(_delete_helpSession)
    return
