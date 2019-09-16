import sys
from flaskApp import db
from flaskApp.models import User
from flaskApp.error.error_handlers import *
from sqlalchemy import text
import string


class DbSearchOptionUtils(object):
    def get_top_results_coursename(param, semester):
        #cursor = db.get_db().cursor()
        query = " select distinct CNum, CName from (select distinct CNum, CName from Course c, Prof_OH po where c.CSID = po.CSID and c.CName \
        <> 'Dissertation Research' and c.CName <> 'PhD Research' and c.CName \
        <> 'Independent Study' and c.CName like '%%%s%%' and c.Semester = '%s' and po.DayTime <> ''\
        union\
        select distinct CNum, CName from Course c, TA_OH t where c.CSID = t.CSID and c.CName \
        <> 'Dissertation Research' and c.CName <> 'PhD Research' and c.CName <> \
        'Independent Study' and c.CName like '%%%s%%' and c.Semester = '%s' and t.DayTime <> '') as temp limit 5" % (param, semester, param, semester)

        sql = text(query)
        resTuple = db.engine.execute(sql)
        result = []
        for item in resTuple:
            print(item[1])
            dictItem = {"id" : item[0], "Name" : item[1]}
            result.append(dictItem)
        #cursor.close()
        return {"result" : result}

    def get_top_results_instructor(param, semester):
        query = "select distinct FName, LName, CNum, CName from (select distinct FName, LName, CNum, CName from Professor p,\
        Teaches te, Prof_OH po, Course c where \
        p.ProfId = te.ProfId and te.CSID = po.CSID and c.CSID = te.CSID and p.LName like '%%%s%%' and c.Semester = '%s' and po.DayTime <> '' \
        union\
        select distinct FName, LName, CNum, CName from Professor p, Teaches te, TA_OH t, Course c where p.ProfId = te.ProfId and te.CSID = t.CSID \
        and te.CSID = c.CSID and\
        p.LName like '%%%s%%' and c.Semester = '%s' and t.DayTime <> '') as temp limit 5" % (param, semester, param, semester)

        sql = text(query)
        resTuple = db.engine.execute(sql)
        result = []
        for item in resTuple:
            print(item[2])
            name = str(item[0]).lstrip().rstrip() + ' ' + str(item[1]).lstrip().rstrip()
            dictItem = {"id" : item[2], "Instructor" : name, "Name" : item[3]}
            result.append(dictItem)
        return {"result" : result}

    def get_top_results_courseID(param, semester):
        query = " select distinct CNum, CName from (select distinct CNum, CName from Course c, Prof_OH po where c.CSID = po.CSID and c.CName \
        <> 'Dissertation Research' and c.CName <> 'PhD Research' and c.CName <> 'Independent Study' \
        and c.CNum like '%%%s%%' and c.Semester = '%s' and po.DayTime <> ''\
        union\
        select distinct CNum, CName from Course c, TA_OH t where c.CSID = t.CSID and c.CName \
        <> 'Dissertation Research' and c.CName <> 'PhD Research' and c.CName <> 'Independent Study'\
        and c.CName like '%%%s%%' and c.Semester = '%s' and t.DayTime <> '') as temp limit 5" % (param, semester, param, semester)

        sql = text(query)
        resTuple = db.engine.execute(sql)
        result = []
        for item in resTuple:
            print(item[0])
            name = str(item[0])
            dictItem = {"id" : item[0], "Name" : item[1]}
            result.append(dictItem)
        return {"result" : result}


    def get_top_results_all_courses(param, semester):
        query = " select distinct CNum, CName from Course where CName \
        <> 'Dissertation Research' and CName <> 'PhD Research' and CName <> 'Independent Study' \
        and CNum like '%%%s%%' and Semester = '%s' limit 5" % (param, semester)

        sql = text(query)
        resTuple = db.engine.execute(sql)
        result = []
        for item in resTuple:
            print(item[0])
            name = str(item[0])
            dictItem = {"id" : item[0], "Name" : item[1]}
            result.append(dictItem)
        return {"result" : result}
