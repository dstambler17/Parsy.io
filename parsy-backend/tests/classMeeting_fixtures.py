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
def create_cal_course_classMeeting(request, db):
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

    classmeet = ClassMeeting(course=courseid, type="Lecture", times="Monday 3:00pm-5:00pm", location="Remsen 104")
    db.session.add(classmeet)
    db.session.commit()
    classmeetId = classmeet.classmeetingId


    def _delete_cal_course_classMeeting():
        classmeet = ClassMeeting.query.filter_by(classmeetingId=classmeetId).first()
        db.session.delete(classmeet)
        db.session.commit()

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_classMeeting)
    return id, courseIDSem, classmeetId

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
def create_cal_course_classMeeting_del(request, db):
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

    classmeet = ClassMeeting(course=course_uuid, type="Lecture", times="Monday 3:00pm-5:00pm", location="Remsen 104")
    db.session.add(classmeet)
    db.session.commit()
    classmeetId = classmeet.classmeetingId

    def _delete_cal_course_classMeeting_del():
        course = Courseitem.query.filter_by(courseuuid=course_uuid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_classMeeting_del)
    return id, coursesSemId, classmeetId


@pytest.fixture
def create_cal_course_classMeeting_del_all(request, db):
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

    classmeet = ClassMeeting(course=courseid, type="Lecture", times="Monday 3:00pm-5:00pm", location="Remsen 104")
    classmeetTwo = ClassMeeting(course=courseid, type="Section", times="Thursday 12:00pm-2:00pm", location="Malone 218")
    db.session.add(classmeet)
    db.session.add(classmeetTwo)
    db.session.commit()
    classmeetId = classmeet.classmeetingId

    def _delete_cal_course_classMeeting_del_all():

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_classMeeting_del_all)
    return id, courseIDSem, classmeetId

@pytest.fixture
def delete_classMeet(request, db):
    def _delete_classMeeting():
        meeting = ClassMeeting.query.filter_by(type="Lecture").first()
        db.session.delete(meeting)
        db.session.commit()

    request.addfinalizer(_delete_classMeeting)
    return

@pytest.fixture
def delete_classMeet_all(request, db):
    def _delete_classMeeting():
        meeting = ClassMeeting.query.filter_by(type="Lecture").all()
        for item in meeting:
            db.session.delete(item)
        db.session.commit()
        meeting_two = ClassMeeting.query.filter_by(type="Section").all()
        for itemtwo in meeting_two:
            db.session.delete(itemtwo)
        db.session.commit()

    request.addfinalizer(_delete_classMeeting)
    return
