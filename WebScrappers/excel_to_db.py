import mysql.connector
import xlrd
import dbInsert
import sys
import OHProcessor

def connectToDB(hostName, db, name, passCode):
    conn = mysql.connector.connect(host= hostName,
                                       database= db,
                                       user= name,
                                       password= passCode)
    print("success")
    return conn

def prof(row, numcols, worksheet, cursor):
    LName = worksheet.cell(row, 1).value.rstrip()
    FName = worksheet.cell(row, 2).value.rstrip()
    email = worksheet.cell(row, 3).value
    dept = worksheet.cell(row, 4).value
    OH = worksheet.cell(row, 6).value
    OH = OHProcessor.processString(OH)
    Loc = ' ' + worksheet.cell(row, 5).value
    #print(LName)
    #print(LName)
    #print(FName)
    #print(email)
    #print(dept)
    #print(OH)
    #print(Loc)
    dbInsert.insertProfDataDB(Loc, OH, email, cursor, LName, FName, dept)
    #print("called")
    #query = "select ProfId from Professor where LName='%s' and FName='%s' and Department = '%s'" % \
     # (LName, FName, dept)
    #print(query)
    #cursor.execute(query)
    #profID = (cursor.fetchone()[0])
    #print(cursor.fetchall())

    #for cols in range(1, numcols):
    #    print(worksheet.cell(row, cols).value)

def TA(row, numcols, worksheet, cursor):
    Loc = ' ' + worksheet.cell(row, 5).value
    OH = worksheet.cell(row, 6).value
    OH = OHProcessor.processString(OH)
    csid = worksheet.cell(row, 7).value + 'spring 2019'
    dbInsert.insertTADataDB(Loc, OH, cursor, csid)
    #print(csid)

    #print('ta ')
    #for cols in range(1, numcols):
    #    print(worksheet.cell(row, cols).value)

def main():
    conn = connectToDB(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    cursor = conn.cursor()
    query_drop_prof = 'drop table if exists Prof_OH'
    query_create_prof = 'create table Prof_OH ( \
    	CSID  	        VARCHAR(30), \
    	DayTime         VARCHAR(200), \
    	LocID  	        VARCHAR(100) \
    )'
    query_drop_TA = 'drop table if exists TA_OH'
    query_create_TA = 'create table TA_OH ( \
    	TEmail          VARCHAR(40), \
    	CSID  	        VARCHAR(30), \
    	DayTime         VARCHAR(300), \
    	LocID  	        VARCHAR(100) \
    )'
    cursor.execute(query_drop_prof)
    cursor.execute(query_create_prof)
    cursor.execute(query_drop_TA)
    cursor.execute(query_create_TA)

    workbook = xlrd.open_workbook('Spring 2019 data.xlsx')
    worksheet = workbook.sheet_by_index(0)
    numrows = worksheet.nrows
    numcols = worksheet.ncols
    print(numrows)
    print(numcols)
    #type = worksheet.cell(0, 1).value
    #print(type)
    for rows in range(0, numrows):
        type = worksheet.cell(rows, 0).value
        if type == 'Prof':
            prof(rows, numcols, worksheet, cursor)
        elif type == 'TA':
            TA(rows, numcols, worksheet, cursor)
            #print("TA")

    conn.commit()
    cursor.close()
    conn.close()




if __name__ == '__main__':
    main()
