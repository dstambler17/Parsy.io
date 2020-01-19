import json
from tests.user_fixtures import *

def test_new_user_201(test_app, delete_user):
    body = {"username" : "test_user", "password" : "password", "affiliation" : "student", "major" : "Computer Science", "school" : "Johns Hopkins", \
    "first_name" : "Dan", "last_name" : "S", "email" : "dsta@gmail.com"}
    url = 'user/new'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res == {}

def test_new_user_400(test_app):
    body = {"username": "test_user", "gibbrish" : "gibby"}
    url = 'user/new'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_new_user_401_badAffiliation(test_app):
    body = {"username" : "test_user", "password" : "password", "affiliation" : "commander"}
    url = 'user/new'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_new_user_401_userExists(test_app, create_user):
    body = {"username" : "test_user", "password" : "password", "affiliation" : "student"}
    url = 'user/new'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_login_201(test_app, create_user):
    body = {"username": "test_user","password": "password"}
    url = 'user/login'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)
    assert r.status_code == 201

def test_login_401_NoUser(test_app, create_user):
    body = {"username": "FakeBoi","password": "password"}
    url = 'user/login'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_login_401_WrongPassword(test_app, create_user):
    body = {"username": "test_user","password": "fakenews"}
    url = 'user/login'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_get_user_data_200(test_app, create_user):
    url = '/user/getInfo/test_user'
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    #assert len(res.keys()) > 0

def test_get_user_data_404(test_app, create_user):
    url = '/user/getInfo/gibbrish'
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_change_password_204(test_app, create_user):
    body = {"new_password" : "newstuff", "password" : "password"}
    url = 'user/change_password/test_user'
    r = test_app.put(url, data=json.dumps(body))

    assert r.status_code == 204

def test_change_password_404(test_app, create_user):
    body = {"new_password" : "newstuff", "password" : "password"}
    url = 'user/change_password/fake_user'
    r = test_app.put(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_change_password_400(test_app, create_user):
    body = {"password" : "password"}
    url = 'user/change_password/test_user'
    r = test_app.put(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 400
    assert res == {'err_msg': 'Bad request'}

def test_change_password_401(test_app, create_user):
    body = {"new_password" : "newstuff", "password" : "fakeNews"}
    url = 'user/change_password/test_user'
    r = test_app.put(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 401
    assert res == {'err_msg': 'Validation failed'}

def test_update_profile_201(test_app, create_user):
    body = {
        'school': 'Harvard',
        'major': 'Having a good time'
    }
    url = 'user/update_profile/test_user'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 201
    assert res['school'] == 'Harvard'
    assert res['major'] == 'Having a good time'

def test_update_profile_404(test_app, create_user):
    body = {
        'school': 'Harvard'
    }
    url = 'user/update_profile/gibbrish'
    r = test_app.post(url, data=json.dumps(body))
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}

def test_get_cals_200(test_app, create_user):
    url = 'user/get_user_cals/test_user'
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    assert len(res) == 0

def test_get_cals_404(test_app, create_user):
    url = 'user/get_user_cals/gibbrish'
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 404
    assert res == {'err_msg': 'Not found'}
