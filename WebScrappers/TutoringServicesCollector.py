import mysql.connector
import requests
import datetime
import json
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from mysql.connector import Error

def requestData(url, headers):
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find("tbody", {"class" : "row-hover"}).find_all("tr")
    days = (rows[0]).find_all("td")
    return rows, days

def parseTable(rows, days):
    del rows[0]
    for row in rows:
        cells = row.find_all("td")
        className = cells[0].get_text()
        print(className)
        for i in range(1, 6):
            if str(cells[i].get_text()) != "":
                entry = str(days[i].get_text()) + " " + str(cells[i].get_text())
                print(entry)
        print(" ")

def getHelpTimes():
    url = "https://advising.jhu.edu/tutoring-mentoring/learning-den-tutoring-services/"
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    rows, days = requestData(url, headers)
    parseTable(rows, days)


    '''
    To insert into DB,
    Insert into Has_Help (Course ID and HelpID), insert into Help (HelpID, Learning Den, Name), insert to Happens_In (help id, daytime, locid)
    '''

def main():
    getHelpTimes()


if __name__ == '__main__':
    main()
