import pytest
import uuid
from flaskApp.models import *

'''@pytest.fixture(scope='module')
def create_user(request, db):
    user = User(username='testUser', password='testpassword')
    db.session.add(user)
    db.session.commit()

    def _delete_user():
        user = User.query.filter_by(username='testUser').first()
        db.session.delete(user)
        db.session.commit()
        pass

    request.addfinalizer(_delete_user)
    return
    '''


@pytest.fixture
def create_cal_delete_session(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.commit()
    id = cal.calID

    def _delete_cal():
        course = Courseitem.query.filter_by(courseID="EN.601.320Spring 2019", calender=id).first()
        course_id = course.courseuuid
        helpsess = HelpSession.query.filter_by(course=course_id).all()
        exams = Exam.query.filter_by(course=course_id).all()
        assignments = Assignment.query.filter_by(course=course_id).all()
        meetings = ClassMeeting.query.filter_by(course=course_id).all()
        for helpses in helpsess:
            db.session.delete(helpses)
            db.session.commit()
        for exam in exams:
            db.session.delete(exam)
            db.session.commit()
        for assignment in assignments:
            db.session.delete(assignment)
            db.session.commit()
        for meeting in meetings:
            db.session.delete(meeting)
            db.session.commit()
        db.session.delete(course)
        db.session.commit()
        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal)
    return id


@pytest.fixture
def create_cal(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.flush()
    id = cal.calID
    db.session.commit()

    def _delete_cal():
        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal)
    return id

@pytest.fixture
def delete_cal(request, db):
    user = User(username='testUser', password='testpassword', affiliation='student')
    db.session.add(user)
    db.session.commit()

    def _delete_cal():
        cal = Calendar.query.filter_by(user='testUser').first()
        db.session.delete(cal)
        db.session.commit()
        user = User.query.filter_by(username='testUser').first()
        db.session.delete(user)
        db.session.commit()

    request.addfinalizer(_delete_cal)
    return


@pytest.fixture
def create_cal_course(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.flush()
    id = cal.calID
    db.session.commit()

    course = Courseitem(courseID="testID", courseName="testName", calender=id, professor="testboi")
    db.session.add(course)
    db.session.flush()
    helpId = course.courseuuid
    db.session.commit()

    def _delete_cal_course():
        helpId = Courseitem.query.filter_by(courseuuid=helpId).first()
        db.session.delete(helpId)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course)
    return id, helpId

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

    helpses = HelpSession(course=courseid, type="testType", times="testTimes", location="testLocation", )
    db.session.add(helpses)
    db.session.commit()
    helpsesId = helpses.helpSessionId

    exam = Exam(course=courseid, type="testType", datetime="testTimes", location="testLocation")
    db.session.add(exam)
    db.session.commit()
    examId = exam.examId

    assignment = Assignment(course=courseid, type="testType", datetime="testTimes", location="testLocation")
    db.session.add(assignment)
    db.session.commit()
    assignmentId = assignment.assignmentId

    classMeeting = ClassMeeting(course=courseid, type="testType", times="testTimes", location="testLocation")
    db.session.add(classMeeting)
    db.session.commit()
    classMeetingId = classMeeting.classmeetingId


    def _delete_cal_course_helpSession():
        helpses = HelpSession.query.filter_by(helpSessionId=helpsesId).first()
        db.session.delete(helpses)
        db.session.commit()

        assignment = Assignment.query.filter_by(assignmentId=assignmentId).first()
        db.session.delete(assignment)
        db.session.commit()

        exam = Exam.query.filter_by(examId=examId).first()
        db.session.delete(exam)
        db.session.commit()

        classMeeting = ClassMeeting.query.filter_by(classmeetingId=classMeetingId).first()
        db.session.delete(classMeeting)
        db.session.commit()

        course = Courseitem.query.filter_by(courseuuid=courseid).first()
        db.session.delete(course)
        db.session.commit()

        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_helpSession)
    return id, helpCourseitem

@pytest.fixture
def delete_course(request, db):
    def _delete_course():
        help = Courseitem.query.filter_by(courseName="Early Modern China").first()
        db.session.delete(help)
        db.session.commit()

    request.addfinalizer(_delete_course)
    return


'''The following is doing some "Del stuff" aka creating but not deleting '''

@pytest.fixture
def create_cal_course_helpSession_del(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.flush()
    id = cal.calID
    db.session.commit()

    course = Courseitem(courseID="testID", courseName="testName", calender=id, professor="testboi")
    db.session.add(course)
    db.session.flush()
    courseuuid = course.courseuuid
    courseID = course.courseID
    db.session.commit()

    helpses = HelpSession(course=courseuuid, type="testType", times="testTimes", location="testLocation")
    db.session.add(helpses)
    db.session.commit()

    exam = Exam(course=courseuuid, type="testType", datetime="testTimes", location="testLocation")
    db.session.add(exam)
    db.session.commit()

    assignment = Assignment(course=courseuuid, type="testType", datetime="testTimes", location="testLocation")
    db.session.add(assignment)
    db.session.commit()

    classMeeting = ClassMeeting(course=courseuuid, type="testType", times="testTimes", location="testLocation")
    db.session.add(classMeeting)
    db.session.commit()

    def _delete_cal_course_helpSession_del():
        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_helpSession_del)
    return id, courseID

@pytest.fixture
def create_cal_course_del(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.flush()
    id = cal.calID
    db.session.commit()

    course = Courseitem(courseID="testID", courseName="testName", calender=id, professor="testboi")
    db.session.add(course)
    db.session.flush()
    helpId = course.courseuuid
    db.session.commit()

    def _delete_cal_course_del():
        cal = Calendar.query.filter_by(calID=id).first()
        db.session.delete(cal)
        db.session.commit()

    request.addfinalizer(_delete_cal_course_del)
    return id, helpId

@pytest.fixture
def create_cal_del(request, db):
    calendaruuid = str(uuid.uuid1())
    cal = Calendar(calID=calendaruuid, user="guest")
    db.session.add(cal)
    db.session.flush()
    id = cal.calID
    db.session.commit()

    return id
