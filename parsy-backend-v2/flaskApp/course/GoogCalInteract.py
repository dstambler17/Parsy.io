from __future__ import print_function
import datefinder
import os.path
import datetime
import pickle
from flaskApp.error.error_handlers import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client import client
from flaskApp.models import User
import httplib2

def create_office_hour_event(service, start_time_str, end_time_str, summary, description, location):
    matchesOne = list(datefinder.find_dates(start_time_str))
    if len(matchesOne):
        start_time = matchesOne[0]
        print(start_time)
    matchesTwo = list(datefinder.find_dates(end_time_str))
    if len(matchesTwo):
        end_time = matchesTwo[0]
        print(end_time)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT=3' #change Count val to match weeks in sem
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

def generate_start_date(weekday, courseID):
    #weekdaytoDateDict = {'Mon': '9 Sept', 'Tu': '3 Sept', 'Wed': '4 Sept', 'Thur' : '5 Sept', 'Fri' : '6 Sept'}
    '''NOTE: Need to make this work for different semesters and make scalable to other schools in terms of start/end dates'''
    if 'Fall' in courseID:
        if 'Mon' in weekday:
            return '9 September'
        elif 'Tu' in weekday:
            return '3 September'
        elif 'Wed' in weekday:
            return '4 September'
        elif 'Thur' in weekday:
            return '5 September'
        elif 'Fri' in weekday:
            return '6 September'
        elif 'Sat' in weekday:
            return '7 September'
        else:
            return '8 September'
    else:
        if 'Mon' in weekday:
            return '3 February 2020'
        elif 'Tu' in weekday:
            return '4 February 2020'
        elif 'Wed' in weekday:
            return '5 February 2020'
        elif 'Thur' in weekday:
            return '6 February 2020'
        elif 'Fri' in weekday:
            return '7 February 2020'
        elif 'Sat' in weekday:
            return '8 February 2020'
        else:
            return '9 February 2020'
class GCalInteract(object):
    def export_cal(res, userid):
        scopes = ['https://www.googleapis.com/auth/calendar']
        creds = None

        '''Get user id here, query for user then get users credentials and convert from json object, then
        just follow the normal flow'''

        user = User.query.filter_by(username=userid[0:20]).first()
        if user is None:
            raise ValidationFailed

        creds = client.Credentials.new_from_json(user.creds)
        #creds.refresh(Request())
        #http_auth = creds.authorize(httplib2.Http())

        #if creds and creds.access_token_expired and creds.refresh_token:
        print("refresh is needed")
        creds.refresh(httplib2.Http())
        print("refresh comp")

        http_auth = creds.authorize(httplib2.Http())
        service = build('calendar', 'v3', http=http_auth)
        #result = service.calendarList().list().execute()
        #print(str(result['items'][0]))
        print(res['content'][0]['support'][0]['location'])
        for course in res['content']:
            summary_start = course['courseName']
            description = None
            courseID = course['courseID']
            for office_hour in course['support']:
                location = office_hour['location']
                summary = summary_start + ' ' + office_hour['type']
                for timePart in office_hour['times'].split(','):
                    dayAndTimeArr = timePart.lstrip().split(' ')
                    day = generate_start_date(dayAndTimeArr[0], courseID)

                    #generate start and end times for util function
                    start = day + ' ' + dayAndTimeArr[1].split('-')[0]
                    end = day + ' ' + dayAndTimeArr[1].split('-')[1]
                    print(start)
                    print(end)
                    create_office_hour_event(service, start, end, summary, description, location)
        #create_office_hour_event(service, '3 June 2pm', '3 June 3:30pm', 'test event', 'this is a test man', 'my place')
        return
