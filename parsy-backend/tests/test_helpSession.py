import json
from tests.helpSession_fixtures import *

def test_get_OH_details_200(test_app, create_cal_course_helpSession):
    (calID, courseIDSem, helpID) = create_cal_course_helpSession
    url = 'helpSession/getOH/' + str(calID) + '/' + str(courseIDSem) + '/' + str(helpID)
    r = test_app.get(url)
    res = json.loads(r.data)

    assert res['times'] == "Thursday 3:00pm-4:30pm"
    assert r.status_code == 200

def test_get_OH_details_404(test_app, create_cal_course_helpSession):
    (calID, courseIDSem, helpID) = create_cal_course_helpSession
    url = 'helpSession/getOH/' + str(calID) + '/' + str(courseIDSem) + '/' + str(12345)
    r = test_app.get(url)
    res = json.loads(r.data)
    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_OH_204_singleitem(test_app, create_cal_course_helpSession_del):
    (calID, courseIDSem, helpsesTime) = create_cal_course_helpSession_del
    url = 'helpSession/deleteOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Thursday 3:00pm-4:30pm", "location" : "Malone 227", "type": "Professor Office Hours"}], "all": "no"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show item got deleted

def test_delete_OH_204_all(test_app, create_cal_course_helpSession_del_all):
    (calID, courseIDSem, helpsesId) = create_cal_course_helpSession_del_all
    url = 'helpSession/deleteOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"id" : helpsesId}], "all": "yes"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show all items got deleted

def test_delete_OH_404_nocourse(test_app, create_cal):
    (calID) = create_cal
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'helpSession/deleteOH/' + str(calID) + '/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_OH_404_nocal(test_app):
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'helpSession/deleteOH/nonsense/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

'''def test_delete_OH_404_nohelpSess(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {"content": [{"time": "Fake News", "location" : "Fake News", "type": "Fake News"}], "all": "no"}
    url = 'helpSession/deleteOH/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}'''

def test_delete_OH_400(test_app, create_cal_course_helpSession):
    (calID, courseIDSem, helpsesId) = create_cal_course_helpSession
    body = {}
    url = 'helpSession/deleteOH/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_restore_OH_201(test_app, create_cal_course, delete_helpSess_all):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'helpSession/restoreOH/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res == {"restore" : "success"}

def test_restore_OH_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'helpSession/restoreOH/' + str(calID) + '/garboge'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_OH_201_individual(test_app, create_cal_course, delete_helpSess):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Thursday 3:00pm-4:30pm", "location" : "Malone 227",\
     "type": "Professor Office Hours"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_OH_201_all(test_app, create_cal_course, delete_helpSess_all):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "yes"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_OH_201_ProfOnly(test_app, create_cal_course, delete_helpSess):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "Prof"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_OH_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/gibbrish'
    body = {"content": [], "all" : "Prof"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_OH_400(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_add_OH_401_ohexists(test_app, create_cal_course_helpSession):
    (calID, courseIDSem, helpId) = create_cal_course_helpSession
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Thursday 3:00pm-4:30pm", "location" : "Malone 227",\
     "type": "Professor Office Hours"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_add_OH_401_notRealOH(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'helpSession/addOH/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Monday 9:00am-5:00pm", "location" : "Malone 227",\
     "type": "Professor Office Hours"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}
