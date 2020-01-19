import json
from tests.assignment_fixtures import *

def test_get_Assignment_details_200(test_app, create_cal_course_assignment):
    (calID, courseIDSem, assignmentID) = create_cal_course_assignment
    url = 'assignment/getAssignment/' + str(calID) + '/' + str(courseIDSem) + '/' + str(assignmentID)
    r = test_app.get(url)
    res = json.loads(r.data)

    assert res['datetime'] == "Tuesday Mar 12th 1:00pm-2:00pm"
    assert r.status_code == 200

def test_get_Assignment_details_404(test_app, create_cal_course_assignment):
    (calID, courseIDSem, assignmentID) = create_cal_course_assignment
    url = 'assignment/getAssignment/' + str(calID) + '/' + str(courseIDSem) + '/' + str(12345)
    r = test_app.get(url)
    res = json.loads(r.data)
    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_Assignment_204_singleitem(test_app, create_cal_course_assignment_del):
    (calID, courseIDSem, assignmentID) = create_cal_course_assignment_del
    url = 'assignment/deleteAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time":"Tuesday Mar 12 1:00pm-2:00pm", "location": "Malone 274", "type": "Homework"}], "all": "no"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show item got deleted

def test_delete_Assignment_204_all(test_app, create_cal_course_assignment_del_all):
    (calID, courseIDSem, assignmentID) = create_cal_course_assignment_del_all
    url = 'assignment/deleteAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"id" : assignmentID}], "all": "yes"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show all items got deleted

def test_delete_Assignment_404_nocourse(test_app, create_cal):
    (calID) = create_cal
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'assignment/deleteAssignment/' + str(calID) + '/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_Assignment_404_nocal(test_app):
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'assignment/deleteAssignment/nonsense/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

'''def test_delete_Assignment_404_noAssignment(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {"content": [{"time":"FakeNews", "location": "Malone 274", "type": "Homework"}], "all": "no"}
    url = 'assignment/deleteAssignment/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}'''

def test_delete_Assignment_400(test_app, create_cal_course_assignment):
    (calID, courseIDSem, assignmentID) = create_cal_course_assignment
    body = {}
    url = 'assignment/deleteAssignment/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_restore_Assignment_201(test_app, create_cal_course, delete_assignmentSlot_all):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'assignment/restoreAssignment/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res == {"restore" : "success"}

def test_restore_Assignment_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'assignment/restoreAssignment/' + str(calID) + '/garboge'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_Assignment_201_individual(test_app, create_cal_course, delete_assignmentSlot_all):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"datetime":"Tuesday Mar 12 1:00pm-2:00pm", "location" : "Malone 274",\
     "type": "Homework"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Assignment_201_all(test_app, create_cal_course, delete_assignmentSlot_all):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "yes"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Assignment_201_Homework_Only(test_app, create_cal_course, delete_assignmentSlot):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "Homework"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Assignment_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/gibbrish'
    body = {"content": [], "all" : "Homework"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_Assignment_400(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_add_Assignment_401_assignmentExists(test_app, create_cal_course_assignment):
    (calID, courseIDSem, assignmentId) = create_cal_course_assignment
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"datetime":"Teusday Mar 12th 1:00pm-2:00pm", "location" : "Malone 274",\
     "type": "Homework"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_add_Assignment_401_notRealAssignment(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'assignment/addAssignment/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Monday 9:00am-5:00pm", "location" : "Malone 227",\
     "type": "Homework"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}
