import re


'''Helper Method: Insert into location'''
def insertLocation(building, room, locid, cursor):
    query = "select LocID from Location where LocID='%s'" % (locid)
    cursor.execute(query)
    loc = cursor.fetchall()
    if not loc:
        LocationInsert = "insert into Location (LocID, Building, Room) values ('%s', '%s', '%s')" % \
          (locid, building, room)
        cursor.execute(LocationInsert)

'''Helper Method: From a raw string, gets the room and building'''
def getLocationInfo(location, cursor):
    rbuild = (str(location)).split(" ")
    building = rbuild[1]
    room = rbuild[2]
    locid = building + room
    insertLocation(building, room, locid, cursor)
    return building, room, locid

'''Helper method: Queries CSIDs from temp table'''
def getCSIDs(Lname, Fname, department, cursor):
    result = []
    query = "select t.CSID from Teaches as t, Professor as p  where p.LName='%s' and p.FName=' %s' \
    and p.Department = '%s' and p.ProfId = t.ProfId" % \
      (Lname, Fname, department)
    cursor.execute(query)
    teachersCourses = cursor.fetchall()
    for course in teachersCourses:
        regEx = re.search('\'(.*)\'', str(course))
        csid = (regEx.group(1)).lower()
        result.append(csid)
    return result

'''Method to insert profInfo to DB'''
def insertProfDataDB(location, officeHours, email, cursor, Lname, Fname, department):
    building, room, locid = getLocationInfo(location, cursor)
    csids = getCSIDs(Lname, Fname, department, cursor)
    ProfessorUpdate = "update Professor SET PEmail='%s' WHERE LName='%s' and FName=' %s' and Department ='%s'" % \
      (email, Lname, Fname, department)
    #LocationInsert = "insert into Location (LocID, Building, Room) values ('%s', '%s', '%s')" % \
     # (locid, building, room)
    statements = [ProfessorUpdate]
    for csid in csids:
        statements.append("insert into Prof_OH (CSID, DayTime, LocID) values ('%s', '%s', '%s')" % \
          (csid, officeHours, locid))

    for sta in statements:
        cursor.execute(sta)

'''Method to insert TAInfo to DB'''
def insertTADataDB(location, officeHours, cursor, csid):
    building, room, locid = getLocationInfo(location, cursor)
    #print(csids)
    TAUpdate = "insert into TA_OH (CSID, DayTime, LocID) values ('%s', '%s', '%s')" % \
      (csid, officeHours, locid)

    cursor.execute(TAUpdate)


'''Method to insert ExamInfo to DB'''
def insertExamDataDB(cursor, csid, name, date):
    #print(csids)
    ExamUpdate = "insert into Exam_Data (CSID, DayTime, Name) values ('%s', '%s', '%s')" % \
      (csid, date, name)

    cursor.execute(ExamUpdate)

'''Method to insert AssignmentInfo to DB'''
def insertAssignmentDataDB(cursor, csid, name, date):
    #print(csids)
    AssignmentUpdate = "insert into Assignment_Data (CSID, DayTime, Name) values ('%s', '%s', '%s')" % \
      (csid, date, name)

    cursor.execute(AssignmentUpdate)
