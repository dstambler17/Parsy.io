import mysql.connector
import dbInsert

def connectToDB(hostName, db, name, passCode):
    conn = mysql.connector.connect(host= hostName,
                                       database= db,
                                       user= name,
                                       password= passCode)
    return conn

def main():
    conn = connectToDB('localhost', 'OH', 'Kevin', 'Qazsewq1!')
    cursor = conn.cursor()

    dbInsert.insertLocation('Malone217', cursor);
    print("success")

    conn.commit()
    cursor.close()
    conn.close()




if __name__ == '__main__':
    main()
