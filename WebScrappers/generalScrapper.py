import mysql.connector
import requests
import datetime
import json
import sys
from mysql.connector import Error
import ASDeptScrapper
#import TutoringServicesCollector

def connectToDB(hostName, db, name, passCode):
    conn = mysql.connector.connect(host= hostName,
                                       database= db,
                                       user= name,
                                       password= passCode)
    return conn

def main():
    '''ASDepartments = {"AS History" : "https://history.jhu.edu/directory/", \
    "AS Classics" : "https://classics.jhu.edu/directory/", \
    "AS Comparative Thought and Literature" : "https://compthoughtlit.jhu.edu/directory/", \
    "AS Near Eastern Studies" : "https://neareast.jhu.edu/directory/", \
    "AS History of Art" : "https://arthist.jhu.edu/directory/", "AS History of Science, Medicine, and Technology" : "https://host.jhu.edu/directory/", \
    "AS Writing Seminars" : "https://writingseminars.jhu.edu/directory/", "AS Sociology" : "https://soc.jhu.edu/directory/", \
    "AS Political Science" : "https://politicalscience.jhu.edu/directory", "AS Anthropology" : "https://anthropology.jhu.edu/directory/", \
    "AS Economics" : "https://econ.jhu.edu/directory/"}'''

    #"AS German %26 Romance Languages %26 Literatures" : "https://grll.jhu.edu/directory/", \
    ASDepartments = {"AS History" : "https://history.jhu.edu/directory/", "AS Economics" : "https://econ.jhu.edu/directory/"}
    conn = connectToDB(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    cursor = conn.cursor()
    query = ("select Lname, FName from Professor where Department = %s")
    for item in ASDepartments:
        cursor.execute(query, (item,))
        teachers = cursor.fetchall()
        ASDeptScrapper.getOH(teachers, ASDepartments[item], cursor, item)
    #TutoringServicesCollector.getHelpTimes()


    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
