import pytest
import uuid
from flaskApp.models import *

@pytest.fixture
def create_cal_course(request, db):
    calendaruuid = str(uuid.uuid4())
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
def create_cal_course_assignment(request, db):
    calendaruuid = str(uuid.uuid4())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    courseid = course.courseuuid
    helpCourseitem = course.courseID

    assignment_slot = Assignment(course=courseid, type="Homework", datetime="Tuesday Mar 12th 1:00pm-2:00pm", location="Malone 274")
    db.session.add(assignment_slot)
    db.session.commit()
    assignment_slotId = assignment_slot.assignmentId


    def _delete_cal_course_assignment():
        assignment_slot = Assignment.query.filter_by(assignmentId=assignment_slotId).first()
        db.session.delete(assignment_slot)
        db.session.commit()

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_assignment)
    return id, helpCourseitem, assignment_slotId

@pytest.fixture
def create_cal(request, db):
    calendaruuid = str(uuid.uuid4())
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
def create_cal_course_assignment_del(request, db):
    calendaruuid = str(uuid.uuid4())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    course_uuid = course.courseuuid
    coursesSemId = course.courseID

    assignment_slot = Assignment(course=course_uuid, type="Homework", datetime="Tuesday Mar 12 1:00pm-2:00pm", location="Malone 274")
    db.session.add(assignment_slot)
    db.session.commit()
    assignment_slotId = assignment_slot.assignmentId

    def _delete_cal_course_assignment_del():
        course = Courseitem.query.filter_by(courseuuid=course_uuid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_assignment_del)
    return id, coursesSemId, assignment_slotId


@pytest.fixture
def create_cal_course_assignment_del_all(request, db):
    calendaruuid = str(uuid.uuid4())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    course = Courseitem(courseID="EN.601.320Spring 2019", courseName="Parallel Programming", calender=id, professor="testboi")
    db.session.add(course)
    db.session.commit()
    courseid = course.courseuuid
    courseIDSem = course.courseID

    assignment_slot = Assignment(course=courseid, type="Homework", datetime="Tuesday Mar 12th 1:00pm-2:00pm", location="Malone 274")
    assignment_slotTwo = Assignment(course=courseid, type="Homework", datetime="Wednesday May 7th 1:00pm-2:00pm", location="Hodson 235")
    db.session.add(assignment_slot)
    db.session.add(assignment_slotTwo)
    db.session.commit()
    assignment_slotId = assignment_slot.assignmentId

    def _delete_cal_course_assignment_del_all():
        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_assignment_del_all)
    return id, courseIDSem, assignment_slotId

@pytest.fixture
def delete_assignmentSlot(request, db):
    def _delete_assignment():
        assignments = Assignment.query.filter_by(type="Homework").all()
        for assignment in assignments:
            db.session.delete(assignment)
        db.session.commit()

    request.addfinalizer(_delete_assignment)
    return

@pytest.fixture
def delete_assignmentSlot_all(request, db):
    def _delete_assignment():
        assignment = Assignment.query.filter_by(type="Homework").all()
        for item in assignment:
            db.session.delete(item)
        db.session.commit()
        assignment_two = Assignment.query.filter_by(type="Homework").all()
        for itemtwo in assignment_two:
            db.session.delete(itemtwo)
        db.session.commit()

    request.addfinalizer(_delete_assignment)
    return
