import json
from tests.classMeeting_fixtures import *

import json
from tests.classMeeting_fixtures import *

def test_get_ClassMeeting_details_200(test_app, create_cal_course_classMeeting):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting
    url = 'classMeeting/getClassMeeting/' + str(calID) + '/' + str(courseIDSem) + '/' + str(meetingId)
    r = test_app.get(url)
    res = json.loads(r.data)

    assert res['times'] == "Monday 3:00pm-5:00pm"
    assert r.status_code == 200

def test_get_ClassMeeting_details_404(test_app, create_cal_course_classMeeting):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting
    url = 'classMeeting/getClassMeeting/' + str(calID) + '/' + str(courseIDSem) + '/' + str(12345)
    r = test_app.get(url)
    res = json.loads(r.data)
    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_ClassMeeting_204_singleitem(test_app, create_cal_course_classMeeting_del):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting_del
    url = 'classMeeting/deleteClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Monday 3:00pm-5:00pm", "location": "Remsen 104", "type": "Lecture"}], "all": "no"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show item got deleted

def test_delete_ClassMeeting_204_all(test_app, create_cal_course_classMeeting_del_all):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting_del_all
    url = 'classMeeting/deleteClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"id" : meetingId}], "all": "yes"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show all items got deleted

def test_delete_ClassMeeting_404_nocourse(test_app, create_cal):
    (calID) = create_cal
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'classMeeting/deleteClassMeeting/' + str(calID) + '/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_ClassMeeting_404_nocal(test_app):
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'classMeeting/deleteClassMeeting/nonsense/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

'''def test_delete_ClassMeeting_404_noclassMeetingSess(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {"content": [{"time": "FakeNews", "location": "Remsen 104", "type": "Lecture"}], "all": "no"}
    url = 'classMeeting/deleteClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}'''

def test_delete_ClassMeeting_400(test_app, create_cal_course_classMeeting):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting
    body = {}
    url = 'classMeeting/deleteClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_restore_ClassMeeting_201(test_app, create_cal_course, delete_classMeet_all):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'classMeeting/restoreClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res == {"restore" : "success"}

def test_restore_ClassMeeting_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'classMeeting/restoreClassMeeting/' + str(calID) + '/garboge'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_ClassMeeting_201_individual(test_app, create_cal_course, delete_classMeet):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"times": "Monday 3:00pm-5:00pm", "location" : "Remsen 104",\
     "type": "Lecture"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_ClassMeeting_201_all(test_app, create_cal_course, delete_classMeet_all):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "yes"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_ClassMeeting_201_LectureOnly(test_app, create_cal_course, delete_classMeet):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "Lecture"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_ClassMeeting_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/gibbrish'
    body = {"content": [], "all" : "Prof"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_ClassMeeting_400(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_add_ClassMeeting_401_ohexists(test_app, create_cal_course_classMeeting):
    (calID, courseIDSem, meetingId) = create_cal_course_classMeeting
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"times": "Monday 3:00pm-5:00pm", "location" : "Remsen 104",\
     "type": "Lecture"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_add_ClassMeeting_401_notRealClassMeeting(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'classMeeting/addClassMeeting/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Monday 9:00am-5:00pm", "location" : "Malone 227",\
     "type": "Lecture"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}
