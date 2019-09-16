import requests
import datetime
import json
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import dbInsert
import OHProcessor

def processName(teacher):
    #regEx = re.search(' (.*)\'', str(teacher))
    #name = (regEx.group(1)).lower()
    temp = (str(teacher)).split("\', \' ")
    Lname = (temp[0].split("\'"))[1]
    Fname = (temp[1].split("\'"))[0]
    FullName = Fname + " " + Lname
    return Lname, Fname, FullName

def buildUrlStandard(teacher, site):
    teacher = teacher.replace(" ", "-")
    return (site + teacher)

def buildUrlFirstLast(teacher, site):
    nameParts = teacher.split(" ")
    FNameLName = nameParts[0] + "-" + nameParts[-1]
    return (site + FNameLName)

def makeRequests(url, headers, name, site):
    r = requests.get(url, headers = headers)
    if r.status_code == 404:
        url = buildUrlFirstLast(name, site)
        r = requests.get(url, headers = headers)
    return r

def scrapeData(text):
    soup = BeautifulSoup(text, 'html.parser')
    profInfo = soup.find("p", {"class" : "listing"})
    regExOne = re.search('fa fa-map-marker-alt\"></span>(.*?)<br/>', str(profInfo))
    regExTwo = re.search('fa fa-calendar\"></span>(.*?)<br/> <', str(profInfo))
    regExThree = re.search(' <a href="mailto:(.*?)\">', str(profInfo))
    if regExOne == None or regExTwo == None or regExThree == None:
        return "", "", ""
    location = (regExOne.group(1))
    officeHours = (regExTwo.group(1))
    email = (regExThree.group(1))
    return location, officeHours, email


def getOH(teachers, site, cursor, department):
    noSiteProfs = []
    for teacher in teachers:
        Lname, Fname, fullName = processName(teacher)
        url = buildUrlStandard(fullName, site)
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        r = makeRequests(url, headers, fullName, site)
        if r.status_code == 200:
            location, officeHours, email = scrapeData(r.text)
            officeHours = OHProcessor.processString(officeHours)
            print(str(location) + " " + str(officeHours) + " " + str(email))
            if(len(location) > 0):
                dbInsert.insertProfDataDB(location, officeHours, email, cursor, Lname, Fname, department)
        else:
            noSiteProfs.append(fullName)
