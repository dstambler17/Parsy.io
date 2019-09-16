import json
from tests.exam_fixtures import *

def test_get_Exam_details_200(test_app, create_cal_course_exam):
    (calID, courseIDSem, examID) = create_cal_course_exam
    url = 'exam/getExam/' + str(calID) + '/' + str(courseIDSem) + '/' + str(examID)
    r = test_app.get(url)
    res = json.loads(r.data)

    assert res['datetime'] == "Monday Mar 11th 1:00pm-2:00pm"
    assert r.status_code == 200

def test_get_Exam_details_404(test_app, create_cal_course_exam):
    (calID, courseIDSem, examID) = create_cal_course_exam
    url = 'exam/getExam/' + str(calID) + '/' + str(courseIDSem) + '/' + str(12345)
    r = test_app.get(url)
    res = json.loads(r.data)
    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_Exam_204_singleitem(test_app, create_cal_course_exam_del):
    (calID, courseIDSem, examID) = create_cal_course_exam_del
    url = 'exam/deleteExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time":"Monday Mar 11 1:00pm-2:00pm", "location": "Malone 274", "type": "Midterm"}], "all": "no"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show item got deleted

def test_delete_Exam_204_all(test_app, create_cal_course_exam_del_all):
    (calID, courseIDSem, examID) = create_cal_course_exam_del_all
    url = 'exam/deleteExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"id" : examID}], "all": "yes"}
    r = test_app.delete(url, data=json.dumps(body))

    assert r.status_code == 204
    #Maybe later have something here to show all items got deleted

def test_delete_Exam_404_nocourse(test_app, create_cal):
    (calID) = create_cal
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'exam/deleteExam/' + str(calID) + '/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_delete_Exam_404_nocal(test_app):
    body = {"content": [{"id" : 123}], "all": "no"}
    url = 'exam/deleteExam/nonsense/FakeNews'
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

'''def test_delete_Exam_404_noExam(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {"content": [{"time":"FakeNews", "location": "Malone 274", "type": "Midterm"}], "all": "no"}
    url = 'exam/deleteExam/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}'''

def test_delete_Exam_400(test_app, create_cal_course_exam):
    (calID, courseIDSem, examID) = create_cal_course_exam
    body = {}
    url = 'exam/deleteExam/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.delete(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_restore_Exam_201(test_app, create_cal_course, delete_examSlot_all):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'exam/restoreExam/' + str(calID) + '/' + str(courseIDSem)
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res == {"restore" : "success"}

def test_restore_Exam_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    body = {}
    url = 'exam/restoreExam/' + str(calID) + '/garboge'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_Exam_201_individual(test_app, create_cal_course, delete_examSlot_all):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"datetime":"Monday Mar 11 1:00pm-2:00pm", "location" : "Malone 274",\
     "type": "Midterm"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Exam_201_all(test_app, create_cal_course, delete_examSlot_all):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "yes"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Exam_201_FinalOnly(test_app, create_cal_course, delete_examSlot):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [], "all" : "Final"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201

def test_add_Exam_404(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/gibbrish'
    body = {"content": [], "all" : "Midterm"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_add_Exam_400(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_add_Exam_401_examExists(test_app, create_cal_course_exam):
    (calID, courseIDSem, examId) = create_cal_course_exam
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"datetime":"Monday Mar 11th 1:00pm-2:00pm", "location" : "Malone 274",\
     "type": "Midterm"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_add_Exam_401_notRealExam(test_app, create_cal_course):
    (calID, courseIDSem) = create_cal_course
    url = 'exam/addExam/' + str(calID) + '/' + str(courseIDSem)
    body = {"content": [{"time": "Monday 9:00am-5:00pm", "location" : "Malone 227",\
     "type": "Midterm"}], "all" : "no"}
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}
