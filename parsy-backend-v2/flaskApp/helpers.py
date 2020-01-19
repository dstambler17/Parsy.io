import string
from sqlalchemy import text
from flaskApp import db
from flaskApp.error.error_handlers import *

def _asdict(obj):
    result = dict()
    for key in obj.__mapper__.c.keys():
        result[key] = getattr(obj, key)
    return result

'''DB querying helper methods to get data'''
def getProfInfo(courseID, semester):
    queryOne = "select distinct C.CSID, C.CName, P.FName, P.LName, P.PEmail \
      From Course as C, Teaches as T, Professor as P \
      WHERE C.CNum = '%s' AND C.Semester = '%s' \
      AND T.CSID = C.CSID AND T.ProfID = P.ProfID GROUP BY P.FName, P.LName" % \
      (courseID, semester)
    sql = text(queryOne)
    courseInfo = db.engine.execute(sql)
    cur = courseInfo.fetchall()
    #print(cur)
    cID = str(cur[0][0])
    cName = str(cur[0][1])
    profName = str(cur[0][2]).lstrip() + " " + str(cur[0][3])
    return cID, cName, profName

def executeOfficeHoursQuery(helpType, courseID, semester):
    #print(courseID)
    #print(semester)
    queryTAs = " select distinct CONCAT('TA', ' Office Hours') as Help, \
     TH.DayTime as DayTime, L.Building, L.Room \
    	FROM Course as C, TA_OH as TH, Location as L \
    	WHERE C.CNum = '%s' AND C.Semester = '%s' AND TH.CSID = C.CSID \
    	AND TH.LocID = L.LocID" % \
        (courseID, semester)

    queryProf = "select distinct 'Professor Office Hours' as Help, P.DayTime as DayTime, L.Building, L.Room \
	FROM Course as C, Prof_OH as P, Location as L \
    WHERE C.CNum = '%s' AND C.Semester = '%s' AND P.CSID = C.CSID AND P.LocID = L.LocID" % \
    (courseID, semester)

    queryHelp = "select distinct He.HName as Help, HI.DayTime as DayTime, L.Building, L.Room \
	FROM Course as C, Has_Help as HH, Help as He, Happens_In as HI, Location as L \
	WHERE C.CNum = '%s' AND C.Semester = '%s' AND HH.CSID = C.CSID AND He.HelpID = HH.HelpID \
	AND HI.HelpID = He.HelpID AND L.LocID = HI.LocID" % \
    (courseID, semester)

    queryTypes = {'prof' : queryProf, 'TA' : queryTAs, 'Other resource' : queryHelp}
    sql = text(queryTypes[helpType])
    results = db.engine.execute(sql)
    return results

def getcourses(courseID, semester):
    helpTypes = ['prof', 'TA', 'Other resource']
    result = []
    for type in helpTypes:
        times = executeOfficeHoursQuery(type,  courseID, semester)
        for time in times:
            loc = str(time[2]) + " " + str(time[3])
            datetimes = time[1]
            datetimes = datetimes[:-1] #remove extra char from Scrapper
            datetimes = datetimes[:-1] #remove extra char from Scrapper

            resultElem = {'type' : time[0], 'times': datetimes, 'location' : loc}
            result.append(resultElem)
    return result

def getCourseIDSemester(param):
    query = "select distinct C.CNum, C.Semester \
      From Course as C \
      WHERE C.CName = '%s'" % \
      (param)
    sql = text(query)
    cur = db.engine.execute(sql)
    resTuple = cur.fetchone()
    if resTuple is None:
        #print("ERROR IN GET COURSE ID SEM")
        raise NotFound
    #print(resTuple)
    cNum = str(resTuple[0])
    Semester = str(resTuple[1])
    return cNum, Semester

def getOHData(param):
    #print(param)
    param = param.lstrip().rstrip() #remove trailing and leading spaces
    #print(param)
    if "null" in param:
        raise NotFound
    #cursor = db.get_db().cursor()
    if "Spring" in param:
        semester = "Spring" + (param.split("Spring"))[1]
        courseID = (param.split("Spring"))[0]
    elif "Fall" in param:
        semester = "Fall" + (param.split("Fall"))[1]
        courseID = (param.split("Fall"))[0]
    else:
        #print(param)
        #print("ERROR IN GET DATA OH")
        raise NotFound
    #print(semester)
    #print(courseID)
    id, cName, prof = getProfInfo(courseID, semester)
    #print(id)
    #print(cName)
    #print(prof)
    courses = getcourses( courseID, semester)
    result = {"id": id, "name" : cName, "prof" : prof, "support" : courses}
    #cursor.close()
    return result

'''End of DB querying methods'''

'''Below is some dummy data until we add the sql to
pull exam info from datapipeline db'''
def getExamData(courseID):
    #print("hi")

    #engine = db.create_engine('mysql://root:Qazsewq1!@localhost/Parsy')
    #select distinct E.CSID, E.Date, E.Time, E.Name from Exam_Data as E where E.CSID = 'EN.601.421'

    res = []
    query = "select distinct E.Date, E.Time, E.Name \
      FROM Exam_Data as E \
      WHERE E.CSID = '%s'" % \
      (courseID)
    query_loc = "select distinct LocID \
      FROM Class_Times \
      WHERE CSID = '%s'" % \
      (courseID)
    query_time = "select distinct DayTime \
      FROM Class_Times \
      WHERE CSID = '%s'" % \
      (courseID)
    if "Spring" in courseID:
        semester = "Spring" + (courseID.split("Spring"))[1]
        courseID = (courseID.split("Spring"))[0]
    elif "Fall" in courseID:
        semester = "Fall" + (courseID.split("Fall"))[1]
        courseID = (courseID.split("Fall"))[0]
    else:
        #print(courseID)
        #print("ERROR IN GET DATA OH")
        raise NotFound
    sql = text(query)
    sql_loc = text(query_loc)
    sql_time = text(query_time)
    results = db.engine.execute(sql)
    results_loc = db.engine.execute(sql_loc)
    results_time = db.engine.execute(sql_time)
    res_exam = []
    exam_location = ""
    exam_time = ""
    for loca in results_loc:
        exam_location = loca[0]
    for t in results_time:
        temp = t[0].index(' ')
        temp = t[0][temp:]
        if ', ' in temp:
            temp = temp[:temp.index(', ')]
        exam_time = temp
    Type = ''
    for exam in results:
        Date = exam[0].strip().capitalize()
        Time = exam[1].strip()
        if Time == '':
            Time = exam_time
        if exam[2].lower() != 'midterm' or exam[2].lower() != 'final':
            if exam[2].lower() == 'final exam':
                Type = 'Final'
            else:
                Type = 'Midterm'
        #Type = exam[2]
        Time = Time.replace(' - ', '-')
        #print("Date: ", Date)
        #print("Time: ", Time)
        #print("Type: ", Type)
        resultExam = {"type": Type, "datetime": Date + Time, "location": exam_location}
        res_exam.append(resultExam)

    id, cName, prof = getProfInfo(courseID, semester)

    res = {"id": id, "name": cName, "prof": prof, "exams": res_exam}
    return res

    '''
    if courseID != "EN.601.320Spring 2019":
        return {"exams" : []}
    res = {"id":"EN.601.320Spring 2019",
    "name":"Parallel Programming",
    "prof":"Randal Burns",
    "exams":[
       {\
          "type":"Midterm",
          "datetime":"Monday March 11 1:00pm-2:00pm",
          "location":"Malone 274"
       },
       {\
          "type":"Midterm",
          "datetime":"Thursday April 2 12:00pm-2:00pm",
          "location":"Malone 218"
       },
       {
          "type":"Final",
          "datetime":"Tuesday May 6 1:00pm-2:00pm",
          "location":"Hodson 235"
       }]}'''
    return res


'''Below is some dummy data until we add the sql to
pull exam info from datapipeline db'''
def getAssignmentData(courseID):
    res = []
    query = "select distinct CSID, Date, Name \
      FROM Assignment_Data \
      WHERE CSID = '%s'" % \
      (courseID)
    query_loc = "select distinct LocID \
      FROM Class_Times \
      WHERE CSID = '%s'" % \
      (courseID)
    query_time = "select distinct DayTime \
      FROM Class_Times \
      WHERE CSID = '%s'" % \
      (courseID)
    if "Spring" in courseID:
        semester = "Spring" + (courseID.split("Spring"))[1]
        courseID = (courseID.split("Spring"))[0]
    elif "Fall" in courseID:
        semester = "Fall" + (courseID.split("Fall"))[1]
        courseID = (courseID.split("Fall"))[0]
    else:
        ###print(courseID)
        #print("ERROR IN GET DATA OH")
        raise NotFound
    sql = text(query)
    sql_loc = text(query_loc)
    sql_time = text(query_time)
    results = db.engine.execute(sql)
    results_loc = db.engine.execute(sql_loc)
    results_time = db.engine.execute(sql_time)
    res_hw = []
    hw_location = ""
    hw_time = ""
    for loca in results_loc:
        hw_location = loca[0]
    for t in results_time:
        temp = t[0].index(' ')
        temp = t[0][temp:]
        if ', ' in temp:
            temp = temp[:temp.index(', ')]
        hw_time = temp
    for hw in results:
        Date = hw[1].strip().capitalize()
        Name = hw[2].strip()
        Time = hw_time
        Time = Time.replace(' - ', '-')
        #Type = exam[2]
        #print("Date: ", Date)
        #print("Name: ", Name)
        resultHW = {"type": 'Homework', "datetime": Date + Time, "location": hw_location}
        res_hw.append(resultHW)

    id, cName, prof = getProfInfo(courseID, semester)

    res = {"id": id, "name": cName, "prof": prof, "assignments": res_hw}
    return res


    '''
    if courseID != "EN.601.320Spring 2019":
        return {"assignments" : []}
    res = {"id":"EN.601.320Spring 2019",
    "name":"Parallel Programming",
    "prof":"Randal Burns",
    "assignments":[
       {\
          "type":"Homework",
          "datetime":"March 12 1:00pm-2:00pm",
          "location":"Malone 274"
       },
       {\
          "type":"Homework",
          "datetime":"April 3 12:00pm-2:00pm",
          "location":"Remsen 217"
       },
       {
          "type":"Homework",
          "datetime":"May 7 1:00pm-2:00pm",
          "location":"Hodson 237"
       }]}
    return res'''

'''Below is some dummy data until we add the sql to
pull class Meeting info from datapipeline db'''
def getClassMeetingData(courseID):
    res = []
    query = "select distinct CSID, DayTime, LocID, Type \
      FROM Class_Times \
      WHERE CSID = '%s'" % \
      (courseID)
    if "Spring" in courseID:
        semester = "Spring" + (courseID.split("Spring"))[1]
        courseID = (courseID.split("Spring"))[0]
    elif "Fall" in courseID:
        semester = "Fall" + (courseID.split("Fall"))[1]
        courseID = (courseID.split("Fall"))[0]
    else:
        #print(courseID)
        #print("ERROR IN GET DATA OH")
        raise NotFound
    sql = text(query)
    results = db.engine.execute(sql)
    res_class = []
    DOW = {'M ':'Monday ', 'T ':'Tuesday ', 'W ':'Wednesday ', 'Th ':'Thursday ', 'F ':'Friday ', 'Sa ':'Saturday ', 'S ':'Sunday '}
    for course in results:
        Times = []
        Times.append(course[1])
        Times_temp = []
        #print("Times: ", Times)
        for time in Times:
            if ', ' in time:
                time = time.split(', ')
                for t in time:
                    Times_temp.append(t)
            else:
                Times_temp.append(time)
        Times = Times_temp
        Times_temp = []
        #print("after comma: ", Times)
        for time in Times:
            #print('time in loop: ', time)
            if 'TTh ' in time:
                temp = time[4:]
                #print('temp: ', temp)
                t = 'Tuesday ' + temp
                Times_temp.append(t)
                t = 'Thursday ' + temp
                Times_temp.append(t)
                #print("ttemp: ", Times_temp)
            elif 'MWF ' in time:
                temp = time[4:]
                #print('temp: ', temp)
                t = 'Monday ' + temp
                Times_temp.append(t)
                t = 'Wednesday ' + temp
                Times_temp.append(t)
                t = 'Friday ' + temp
                Times_temp.append(t)
                #print("ttemp: ", Times_temp)
            elif 'MW ' in time:
                #print('I am in MW')
                temp = time[3:]
                #print('temp: ', temp)
                t = 'Monday ' + temp
                Times_temp.append(t)
                t = 'Wednesday ' + temp
                Times_temp.append(t)
                #print("ttemp: ", Times_temp)
            else:
                Times_temp.append(time)
        #print("Times_Temp: ", Times_temp)
        Times = Times_temp
        #print("New Times: ", Times)
        LocID = course[2]
        Type = course[3]
        #print("time: ", Times)
        #print("Location: ", LocID)
        #print("Type: ", Type)
        for time in Times:
            if time[:3] in DOW.keys():
                time = DOW[time[:3]] + time[3:]
            elif time[:2] in DOW.keys():
                time = DOW[time[:2]] + time[2:]
            if ' - ' in time:
                time = time.replace(' - ', '-')
            resultClass = {"type": Type, "times": time, "location": LocID}
            res_class.append(resultClass)

    id, cName, prof = getProfInfo(courseID, semester)

    res = {"id": id, "name": cName, "prof": prof, "meetings": res_class}
    return res

    '''
    if courseID != "EN.601.320Spring 2019":
        return {"meetings" : []}
    res = {"id":"EN.601.320Spring 2019",
    "name":"Parallel Programming",
    "prof":"Randal Burns",
    "meetings":[
       {\
          "type":"Lecture",
          "times":"Monday 3:00pm-5:00pm",
          "location":"Remsen 104"
       },
       {\
          "type":"Section",
          "times":"Thursday 12:00pm-2:00pm",
          "location":"Malone 218"
       }]}
    return res'''
