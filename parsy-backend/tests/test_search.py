import pytest
import json

def test_search_suggestions_class_name(test_app):
    url = "searchOption/className/Spring 2019/sov"
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    assert "Soviet-American Cold War" in res['result'][0]["Name"]

def test_search_suggestions_instructor(test_app):
    url = "searchOption/instName/Spring 2019/se"
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    assert "Joanne F Selinski" in res['result'][0]["Instructor"]

def test_search_suggestions_id(test_app):
    url = "searchOption/courseID/Spring 2019/EN.601.3"
    r = test_app.get(url)
    res = json.loads(r.data)

    assert r.status_code == 200
    assert "EN.601.320" in res['result'][0]["id"]
