import json
from tests.course_fixtures import *

def test_new_cal_201(test_app, delete_cal):
    sample = {'username' : 'testUser'}
    url = 'course/newCal'
    r = test_app.post(url, data=json.dumps(sample))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert isinstance(res, dict)

def test_new_cal_400(test_app):
    sample = {}
    url = 'course/newCal'
    r = test_app.post(url, data=json.dumps(sample))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_new_cal_404(test_app):
    sample = {"username": "fakenews"}
    url = 'course/newCal'
    r = test_app.post(url, data=json.dumps(sample))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_get_cal_200(test_app, create_cal):
    url = 'course/' + str(create_cal)
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    assert res['user'] == 'guest'

def test_get_cal_404(test_app):
    url = 'course/notarealid'
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_cal_204(test_app, create_cal_del):
    url = 'course/' + str(create_cal_del)
    r = test_app.delete(url)

    assert r.status_code == 204

def test_delete_cal_404(test_app):
    url = 'course/fakecal'
    r = test_app.delete(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_session_201(test_app, create_cal_delete_session):
    url = 'course/' + str(create_cal_delete_session) + '/addClassHelp/EN.601.320Spring 2019'
    r = test_app.post(url)
    #res = json.loads(r.data)

    assert r.status_code == 201
    #assert res['id'] == "AS.100.347Spring 2019"

def test_add_session_404_calError(test_app, create_cal):
    url = 'course/fakeCal/addClassHelp/Early Modern China'
    r = test_app.post(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_session_404_item_courseIDError(test_app, create_cal):
    url = 'course/' + str(create_cal) + '/addClassHelp/fakeClass'
    r = test_app.post(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_session_401(test_app, create_cal_course_helpSession):
    (id, coursecourse) = create_cal_course_helpSession
    url = 'course/' + str(id) + '/addClassHelp/EN.601.320Spring 2019'
    r = test_app.post(url)
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_delete_session_204(test_app, create_cal_course_helpSession_del):
    (id, course_name) = create_cal_course_helpSession_del
    url = 'course/' + str(id) + '/removeClass/' + str(course_name)
    r = test_app.delete(url)

    assert r.status_code == 204

def test_delete_session_404_calError(test_app, create_cal_course_helpSession):
    (cal_id, course_id) = create_cal_course_helpSession
    url = 'course/fakeCal/removeClass/' + str(course_id)
    r = test_app.delete(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_session_404_courseIDError(test_app, create_cal_course_helpSession):
    (cal_id, course_id) = create_cal_course_helpSession
    url = 'course/' + str(cal_id) + '/removeClass/fakeHelp'
    r = test_app.delete(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_get_session_404(test_app):
    url = "helpSession/getTest/fakeStuff"
    r = test_app.get(url)
    res = json.loads(r.data)
    assert r.status_code == 404

def test_get_session(test_app):
    url = "helpSession/getTest/EN.601.320Spring 2019"
    r = test_app.get(url)
    res = json.loads(r.data)

    assert res['id'] == "EN.601.320Spring 2019"
    assert res['prof'] == "Randal Burns"
