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


def siftData(data):
    teachers = []
    for i in range(0, len(data)):
        teacher = data[i]["InstructorsFullName"]
        courseNum = data[i]["OfferingName"]
        courseName = cleanData(data[i]["Title"])
        term = data[i]["Term"]
        CSID = str(courseNum) + term
        if "," not in teacher:
            continue
        flnames = teacher.split(",")
        alphabetTeach = [flnames[1], flnames[0], courseName, courseNum, term, CSID]
        if alphabetTeach not in teachers:
            teachers.append(alphabetTeach)
    #teachers.sort()
    return teachers


def checkSchool(department):
    schools = ["Krieger School of Arts and Sciences", "Whiting School of Engineering"]
    if (department.split(" "))[0] == "AS":
        return schools[0]
    elif (department.split(" "))[0] == "EN":
        return schools[1]

def makeUrl(department):
    url = "https://sis.jhu.edu/api/classes/?key=vnv3AWClXNW2CC52Ek2HfN5EdKyp2m2g&School="
    url = url + checkSchool(department) + "&Department=" + department + "&Term=fall%202019&level=Upper%20Level%20Undergraduate&level=lower%20level%20undergraduate&level=Graduate"
    return url

def removeExtranCourse(course):
    if course == "Graduate Research" or course == "Dissertation Research" or course == "Masters Research" \
    or course == "Trial Research Paper I"  or course == "Trial Research Paper II" or course == "Teaching Assistantship" \
    or course == "Dissertation Fellowship Semester" or  "Independent Study" in course or course == "Research Apprenticeship" \
    or course == "Research Assistantship" or course == "Individual work" or course == "Independent Research-Graduate" \
    "Graduate Research" in course or course == "PhD Research" or course == "Special Research/Problems" or course == "Readings and Research" \
    or "Independent Stdy" in course or "Dissertation" in course or "Proposal Prep" in course or "Thesis" in course or "Paper Presentation" in course:
        return True

    return False

def insertPreliminaryData(cursor, instructorInfo, department, num_queries):
    if removeExtranCourse(instructorInfo[2]):
        return num_queries

    if '\'' in instructorInfo[0]:
        instructorInfo[0] = instructorInfo[0].replace('\'', "\\'")
    elif '\'' in instructorInfo[1]:
        instructorInfo[1] = instructorInfo[1].replace('\'', "\\'")
    query = "select ProfId from Professor where LName='%s' and FName='%s' and Department = '%s'" % \
      (instructorInfo[1], instructorInfo[0], department)
    cursor.execute(query)
    teacherID = cursor.fetchone()
    if teacherID is None:
        profInsert  = "insert into Professor (LName, FName, PEmail, Department) values('%s', '%s', null, '%s')" % \
          (instructorInfo[1], instructorInfo[0], department)
        cursor.execute(profInsert)
        cursor.execute("SELECT LAST_INSERT_ID()")
        teacherID = cursor.fetchone()

        num_queries = num_queries + 2

    courseInsert = "insert into Course (CSID, CName, CNum, Semester) values ('%s', '%s', '%s', '%s')" % \
      (instructorInfo[5], instructorInfo[2], instructorInfo[3], instructorInfo[4])
    teachesInsert = "insert into Teaches (ProfId, CSID) values ('%d', '%s')" % \
      (teacherID[0], instructorInfo[5])
    #prof_OHInsert = "insert into Prof_OH (CSID, DayTime, LocID) values ('%s', null, null)" % \
     # (instructorInfo[5].lower())

    statements = [courseInsert, teachesInsert]
    for sta in statements:
        cursor.execute(sta)
    num_queries = num_queries + 3
    return num_queries


def main():
    departments = ["EN Computer Science", "AS Mathematics", "EN Chemical %26 Biomolecular Engineering", \
        'AS Economics', 'AS History', \
        'EN Applied Mathematics %26 Statistics'] #only depts added on 2/18/19 will add more later
    '''departments = ["EN Computer Science", "AS Mathematics", "EN Chemical %26 Biomolecular Engineering", \
       "AS Biology", "EN Biomedical Engineering", "AS Chemistry", "EN Electrical %26 Computer Engineering", \
       "EN Applied Mathematics %26 Statistics", "EN Mechanical Engineering", "AS Neuroscience", "AS Physics %26 Astronomy", \
        "AS History", "AS Economics", "AS Classics", "AS Comparative Thought and Literature", \
        "AS Near Eastern Studies"] '''
     #The below table is to be run 1 hour later due to db max ques limit
     #departments = ["AS History of Art", "AS History of Science, Medicine, and Technology", "AS Writing Seminars", \
     # "AS Sociology", "AS Anthropology", "AS Political Science", "AS Economics"]
     #"AS International Studies", "AS German %26 Romance Languages %26 Literatures"]

    conn = connectToDB(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    #localhost, myAssist Dan, asdfg
    cursor = conn.cursor()
    num_queries = 0

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


if __name__ == '__main__':
    main()
