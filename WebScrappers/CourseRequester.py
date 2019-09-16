import mysql.connector
import requests
import datetime
import json
import sys
from mysql.connector import Error

def connectToDB(hostName, db, name, passCode):
    conn = mysql.connector.connect(host= hostName,
                                       database= db,
                                       user= name,
                                       password= passCode)
    return conn
    

def cleanData(item):
    new = item.replace("\'", "\"")
    return new


def siftDataDept(data):
    departments = []
    for i in range(0, len(data)):
        dept = data[i]["DepartmentName"]
        departments.append(dept)
    return departments

def siftDataCourses(data):
    cName = []
    cNum = []
    cProf = []
    cTime = []
    cLoc = []
    cBuilding = []
    cType = []
    cDept = []
    courses = []
    for i in range(0, len(data)):
        if data[i]["InstructionMethod"] == "Independent Study":
            continue
        cName.append(data[i]["Title"])
        cNum.append(data[i]["OfferingName"])
        cProf.append(data[i]["InstructorsFullName"])
        cTime.append(data[i]["Meetings"])
        cLoc.append(data[i]["Location"])
        cBuilding.append(data[i]["Building"])
        cType.append(data[i]["InstructionMethod"])
        cDept.append(data[i]["Department"])
    for i in range(0, len(cNum)):
        course = {"ID": cNum[i], "Name": cName[i], "Prof": cProf[i], "Time": cTime[i], "Location": cLoc[i], "Building": cBuilding[i], "Type": cType[i], "Department": cDept[i]}
        courses.append(course)
        print(cNum[i])
        print(cTime[i])
    return courses

def makeURL(school, term):
    API_URL = 'https://sis.jhu.edu/api/classes'
    API_KEY = 'ZzJuREPYxUQWYETkdmRCZg7hg7qN5wFS'
    URL = API_URL + '/' + school + '/' + term + '?key=' + API_KEY
    return URL

def main():
    term = "Fall 2019"
    schools = ["Krieger School of Arts and Sciences", "Whiting School of Engineering"]
    departments = []
    r_WSE_dept = requests.get('https://sis.jhu.edu/api/classes/codes/departments/Whiting%20School%20of%20Engineering?key=ZzJuREPYxUQWYETkdmRCZg7hg7qN5wFS')
    r_KSAS_dept = requests.get('https://sis.jhu.edu/api/classes/codes/departments/Krieger School of Arts and Sciences?key=ZzJuREPYxUQWYETkdmRCZg7hg7qN5wFS')
    data_WSE_dept = json.loads(r_WSE_dept.text)
    data_KSAS_dept = json.loads(r_KSAS_dept.text)
    departments_WSE = siftDataDept(data_WSE_dept)
    #print(departments_WSE)
    departments_KSAS = siftDataDept(data_KSAS_dept)
    #print(departments_WSE)
    URL_WSE = makeURL("Whiting School of Engineering", term)
    URL_KSAS = makeURL("Krieger School of Arts and Sciences", term)
    r_WSE = requests.get(URL_WSE)
    r_KSAS = requests.get(URL_KSAS)
    data_WSE = json.loads(r_WSE.text)
    data_KSAS = json.loads(r_KSAS.text)
    WSE_Courses = siftDataCourses(data_WSE)
    KSAS_Courses = siftDataCourses(data_KSAS)



    conn = connectToDB('parsyio-db.cnnzxrdujotc.us-east-1.rds.amazonaws.com', 'parsy', 'parsyioadmin', 'DanKevDave2020')
    #conn = connectToDB(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    #localhost, myAssist Dan, asdfg
    cursor = conn.cursor()

    for i in range(0, len(WSE_Courses)):
        ClassTimesUpdate = "insert into Class_Times (CSID, DayTime, LocID, Type) values ('%s', '%s', '%s', '%s')" % \
            (WSE_Courses[i]["ID"]+term, WSE_Courses[i]["Time"], WSE_Courses[i]["Building"], WSE_Courses[i]["Type"])
        cursor.execute(ClassTimesUpdate)
    for i in range(0, len(KSAS_Courses)):
        ClassTimesUpdate = "insert into Class_Times (CSID, DayTime, LocID, Type) values ('%s', '%s', '%s', '%s')" % \
            (KSAS_Courses[i]["ID"]+term, KSAS_Courses[i]["Time"], KSAS_Courses[i]["Building"], KSAS_Courses[i]["Type"])
        cursor.execute(ClassTimesUpdate)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    
    '''

    delTable = "drop table if exists Temp"
    makeTempTable = "create table Temp ( CSID VARCHAR(30), LName VARCHAR(25), \
      FName VARCHAR(25), Department VARCHAR(40))"
    cursor.execute(delTable)
    cursor.execute(makeTempTable)

    profs = ""
    for item in departments:
        url = makeUrl(item)
        print(url)
        r = requests.get(url)
        data = json.loads(r.text)
        instructors = siftData(data)
        for i in instructors:
            if str(i[0])+str(i[1]) not in profs:
                profs+=(str(i[0])+' '+str(i[1])+'\n')
        for elem in instructors:
            num_queries = insertPreliminaryData(cursor, elem, item, num_queries)
    f = open('prof_list', 'w')
    f.write(profs)
    f.close()
    test = ""
    test += "hi "
    test += "there"
    test += "!"
    print(test)
    print(str(num_queries))
    conn.commit()
    cursor.close()
    conn.close()
    '''


if __name__ == '__main__':
    main()