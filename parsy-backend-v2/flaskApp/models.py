from flaskApp import db
from datetime import datetime
#from sqlalchemy.dialects.postgresql import UUID
#import uuid
import json
import sqlalchemy
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from sqlalchemy import PrimaryKeyConstraint


SIZE = 256
class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.String(128))
    affiliation = db.Column(db.String(20), nullable=False) #Prof/Student/Admin?
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    major = db.Column(db.String(128))
    school = db.Column(db.String(128))
    email = db.Column(db.String(128))
    creds = db.Column(TextPickleType())

    def __repr__(self):
        return 'User info: %s, %s' % (self.username, self.email)

class School(db.Model):
    school_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    alias = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(200), nullable=False) #Ex: Peabody vs AS. This is because different schools have different start and end dates for classes
    PrimaryKeyConstraint('name', 'program', name='school_pk')

    def __repr__(self):
        return 'User info: %s, %s' % (self.name, self.program)

'''Keeps the start and end times for each semester for each year'''
class SemesterStartEndTimes(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    school_id = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.String(200), nullable=False)
    end_date = db.Column(db.String(200), nullable=False)
    PrimaryKeyConstraint('school_id', 'semester', name='semester_start_end_date_pk')


class Calendar(db.Model):
    calID = db.Column(db.String(40), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(20), db.ForeignKey("user.username"))
    school_id =db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return 'Calendar info: %s, %s, %s' % (self.calID, self.user, self.content)

class Courseitem(db.Model):
    courseuuid = db.Column(db.Integer, primary_key=True, nullable=False)
    courseID = db.Column(db.String(30), nullable=False)
    calender = db.Column(db.String(40), db.ForeignKey("calendar.calID"), nullable=False)
    courseName = db.Column(db.String(50), nullable=False)
    professor = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Courseitem info: %s, %s, %s' % (self.courseuuid, self.calender, self.courseID)

'''Slot is the refactored, helpSession, Exam, Assignment, Classmeeting, rolled into one Model
The reasoning behind this is that the other four models are really similar and the code reuse in the slots
are near identical'''
class Slot(db.Model):
    slot_id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(40), nullable=False) #Assignment, Exam, ClassTime, HelpSession
    sub_type = db.Column(db.String(40), nullable=False) #I.E prof, TA, learning den, Midterm, Final, Quiz, Homework, Lecture, section, lab
    is_weekly = db.Column(db.Boolean, nullable=False) #True for ClassTime/HelpSession
    time = db.Column(db.String(200)) #Either something like 'Monday Mar 11 1:00pm-2:00pm' or 'Monday 3:00pm-5:00pm' for weekly
    location = db.Column(db.String(200))

class HelpSession(db.Model):
    helpSessionId = db.Column(db.Integer, primary_key=True, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courseitem.courseuuid"), nullable=False)
    type = db.Column(db.String(40), nullable=False) #I.E prof, TA, or learning den, etc
    times = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return 'HelpSession info: %s, %s, %s, %s' % (self.helpSessionId, self.course, self.times, self.location)

class Exam(db.Model):
    examId = db.Column(db.Integer, primary_key=True, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courseitem.courseuuid"), nullable=False)
    type = db.Column(db.String(20)) #I.E Midterm or Final
    weight = db.Column(db.String(20)) #How much worth of final grade is this exam
    datetime = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return 'Exam info: %s, %s, %s, %s' % (self.examId, self.course, self.datetime, self.location)

class Assignment(db.Model):
    assignmentId = db.Column(db.Integer, primary_key=True, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courseitem.courseuuid"), nullable=False)
    type = db.Column(db.String(20)) #I.E Homework
    weight = db.Column(db.String(20)) #How much worth of final grade is this exam
    datetime = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return 'Assignment info: %s, %s, %s, %s' % (self.assignmentId, self.course, self.datetime, self.location)


class ClassMeeting(db.Model):
    classmeetingId = db.Column(db.Integer, primary_key=True, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courseitem.courseuuid"), nullable=False)
    type = db.Column(db.String(20)) #Lecture, section, lab
    times = db.Column(db.String(200)) #happens everyweek
    location = db.Column(db.String(200))

    def __repr__(self):
        return 'Note info: %s, %s, %s, %s' % (self.classmeetingId, self.course, self.times, self.location)

class EmailSubscriber(db.Model):
    emailsubid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))

    def __repr__(self):
        return 'Info: %s, %s' % (self.name, self.email)

class Report(db.Model):
    reportid = db.Column(db.Integer, primary_key=True, nullable=False)
    courseID = db.Column(db.String(30))
    semester = db.Column(db.String(15))
    url = db.Column(db.String(250))
    status = db.Column(db.String(15)) #success, otherwise blank

    def __repr__(self):
        return 'Info: %s, %s' % (self.courseID, self.status)
