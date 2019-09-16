import sys
from flask import Blueprint, request, jsonify
from flaskApp import db
from flaskApp.searchOption.utils import *
from flaskApp.error.error_handlers import *
import json

searchOption = Blueprint('searchOption', __name__)

@searchOption.route('className/<semester>/<wordInput>', methods=['GET'])
def get_search_suggestions_coursename(wordInput, semester):
    param = wordInput.lstrip().rstrip()
    result = DbSearchOptionUtils.get_top_results_coursename(param, semester)
    return jsonify(result)
''' Use this sql line:
select distinct CName from course c, prof_oh po where c.CSID = po.CSID and c.CName
<> "Dissertation Research" and c.CName <> "Independent Study" and c.CName like "S%"; '''

@searchOption.route('instName/<semester>/<wordInput>', methods=['GET'])
def get_search_suggestions_instructor(wordInput, semester):
    param = wordInput.lstrip().rstrip()
    result = DbSearchOptionUtils.get_top_results_instructor(param, semester)
    return jsonify(result)

@searchOption.route('courseID/<semester>/<wordInput>', methods=['GET'])
def get_search_suggestions_courseIDSem(semester, wordInput):
    param = wordInput.lstrip().rstrip()
    result = DbSearchOptionUtils.get_top_results_courseID(param, semester)
    return jsonify(result)

@searchOption.route('allCourseID/<semester>/<wordInput>', methods=['GET'])
def get_search_suggestions_from_all_courses(semester, wordInput):
    param = wordInput.lstrip().rstrip()
    result = DbSearchOptionUtils.get_top_results_all_courses(param, semester)
    return jsonify(result)
