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
def create_cal_course_exam(request, db):
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

    exam_slot = Exam(course=courseid, type="Midterm", datetime="Monday Mar 11th 1:00pm-2:00pm", location="Malone 274")
    db.session.add(exam_slot)
    db.session.commit()
    exam_slotId = exam_slot.examId


    def _delete_cal_course_exam():
        exam_slot = Exam.query.filter_by(examId=exam_slotId).first()
        db.session.delete(exam_slot)
        db.session.commit()

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_exam)
    return id, helpCourseitem, exam_slotId

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
def create_cal_course_exam_del(request, db):
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

    exam_slot = Exam(course=course_uuid, type="Midterm", datetime="Monday Mar 11 1:00pm-2:00pm", location="Malone 274")
    db.session.add(exam_slot)
    db.session.commit()
    exam_slotId = exam_slot.examId

    def _delete_cal_course_exam_del():
        course = Courseitem.query.filter_by(courseuuid=course_uuid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_exam_del)
    return id, coursesSemId, exam_slotId


@pytest.fixture
def create_cal_course_exam_del_all(request, db):
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

    exam_slot = Exam(course=courseid, type="Midterm", datetime="Monday Mar 11th 1:00pm-2:00pm", location="Malone 274")
    exam_slotTwo = Exam(course=courseid, type="Final", datetime="Tuesday May 6th 1:00pm-2:00pm", location="Hodson 235")
    db.session.add(exam_slot)
    db.session.add(exam_slotTwo)
    db.session.commit()
    exam_slotId = exam_slot.examId

    def _delete_cal_course_exam_del_all():
        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_exam_del_all)
    return id, courseIDSem, exam_slotId

@pytest.fixture
def delete_examSlot(request, db):
    def _delete_exam():
        exam = Exam.query.filter_by(type="Final").first()
        db.session.delete(exam)
        db.session.commit()

    request.addfinalizer(_delete_exam)
    return

@pytest.fixture
def delete_examSlot_all(request, db):
    def _delete_exam():
        exam = Exam.query.filter_by(type="Midterm").all()
        for item in exam:
            db.session.delete(item)
        db.session.commit()
        exam_two = Exam.query.filter_by(type="Final").all()
        for itemtwo in exam_two:
            db.session.delete(itemtwo)
        db.session.commit()

    request.addfinalizer(_delete_exam)
    return
