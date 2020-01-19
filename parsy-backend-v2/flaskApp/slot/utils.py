import sys
from flaskApp import db
from flaskApp.models import Slot, Courseitem, Calendar
from flaskApp.error.error_handlers import *
from sqlalchemy import text
from flaskApp.helpers import _asdict, getAssignmentData, getClassMeetingData, getOHData, getExamData
import string

class ObjectChecks(object):
    def check_cal(cal_Id):
        cal = Calendar.query.filter_by(calID=cal_Id).first()
        if cal is None:
            raise NotFound
        return cal

    def check_course(cal_Id, course_ID):
        course = Courseitem.query.filter_by(courseID=course_ID, calender=cal_Id).first()
        if course is None:
            raise NotFound
        return course

    def check_slot_time(timeslot_id):
        timeslot = Slot.query.filter_by(slot_id=timeslot_id).first()
        if timeslot is None:
            raise NotFound
        return timeslot

    def check_slot_time_del(slot_type, time, location, sub_type, course_uuid):
        timeslot = Slot.query.filter_by(time=time, location=location, type=slot_type, sub_type=sub_type, course=course_uuid).first()
        if timeslot is None:
            return None
        return timeslot

    def check_contains_slot(slot_type, sub_type, course, time, location):
        timeslot = Slot.query.filter_by(course=course, type=slot_type, subtype=sub_type, time=time, location=location).first()
        if timeslot is not None:
            raise ValidationFailed

class SlotUtils:
    def get_slot_func_and_weekly(slot_type):
        func_dict ={'support' :  getOHData, 'exams' : getExamData, 'assignments' : getAssignmentData, 'meetings' : getClassMeetingData}
        is_weekly = True if slot_type in ['support', 'meetings'] else False
        return func_dict[slot_type], is_weekly

    '''Methods for adding Slots'''
    def add_all_slots(courseID, course_uuid, slot_type):
        res = {"added" : []}
        func, is_weekly = SlotUtils.get_slot_func_and_weekly(slot_type)
        data = func(courseID)
        timeslots = data['Slots']
        for item in timeslots:
            subtype = item["subtype"]
            time = item["time"]
            location = item["location"]
            ObjectChecks.check_contains_slot(slot_type, subtype, course_uuid, time, location)
            slot = Slot(course=course_uuid, is_weekly=is_weekly, sub_type = subtype, type=slot_type, time=time, location=location)
            res["added"].append(_asdict(slot))
            db.session.add(slot)
        db.session.commit()
        return res

    def add_slot_based_on_type(courseID, course_uuid, slot_sub_type, slot_type):
        res = {"added" : []}
        func, is_weekly = SlotUtils.get_slot_func_and_weekly(slot_type)
        data = func(courseID)
        timeslots = data['slots']
        for item in timeslots:
            sub_type = item["type"]
            time = item["time"]
            location = item["location"]
            if slot_sub_type in sub_type:
                slot_check = Slot.query.filter_by(course=course_uuid, type=slot_type, sub_type=sub_type, time=time, location=location).first()
                if slot_check is None:
                    slot = Slot(course=course_uuid, is_weekly=is_weekly, sub_type = sub_type, type=slot_type, time=time, location=location)
                    db.session.add(slot)
                    res["added"].append(_asdict(slot))
        db.session.commit()
        return res

    def validate_slot_input(courseID, course_uuid, content, slots):
        slotList = []
        for item in slots:
            type = item["type"]
            time = item["time"]
            location = item["location"]
            dictItem = {"time": time, "location" : location, "type": type}
            slotList.append(dictItem)
        for slot in content:
            if slot not in slotList:
                raise ValidationFailed

    def delete_all_slots(course_uuid, slot_type):
        slots = Slot.query.filter_by(course=course_uuid, type=slot_type).all()
        for slot in slots:
            db.session.delete(slot)
        db.session.commit()

class DbSlotInteract(object):
    def get_slot_details(calID, courseID, slot):
        check_cal(calID)
        check_course(calID, courseID)
        timeslot = check_slot_time(slot)
        res = _asdict(timeslot)
        return res

    def add_slot(calID, courseID, request_body):
        MAIN_SLOT_TYPES = ['support', 'exams', 'assignments', 'meetings']
        CATAGORIES = ['Homework', 'Prof', 'TA', 'Lecture', 'Section', 'Lab', 'Midterm', 'Final', 'Quiz']
        ObjectChecks.check_cal(calID)
        course = ObjectChecks.check_course(calID, courseID)
        course_ID_sem = course.courseID
        course_uuid = course.courseuuid
        if 'content' not in request_body or 'all' not in request_body or 'type' not in request_body:
            raise BadRequest
        if request_body['type'] not in MAIN_SLOT_TYPES:
            raise BadRequest
        if request_body['all'] == 'yes':
            res = SlotUtils.add_all_slots(course_ID_sem, course_uuid, request_body['type'])
            return res
        elif request_body['all'] in CATAGORIES:
            res = SlotUtils.add_slot_based_on_type(course_ID_sem, course_uuid, request_body['all'], request_body['type'])
            return res
        else:
            res = {"added" : []}
            func, is_weekly = SlotUtils.get_slot_func_and_weekly(request_body['type'])
            data = func(course_ID_sem)
            in_db_slots = data[request_body['type']]
            content = request_body['content']
            SlotUtils.validate_slot_input(course_ID_sem, course_uuid, content, in_db_slots)
            for item in content:
                ObjectChecks.check_contains_slot(request_body['type'], item['type'], course_uuid, item['time'], item['location'])
                slot = Slot(course=course_uuid, type=item['type'], time=item['time'], location=item['location'], is_weekly=is_weekly, sub_type=item['sub_type'])
                db.session.add(slot)
                res["added"].append(_asdict(slot))
            db.session.commit()
            return res

    def delete_slot(calID, courseID, request_body):
        ObjectChecks.check_cal(calID)
        MAIN_SLOT_TYPES = ['support', 'exams', 'assignments', 'meetings']
        CATAGORIES = ['Homework', 'Prof', 'TA', 'Lecture', 'Section', 'Lab', 'Midterm', 'Final', 'Quiz']
        course = ObjectChecks.check_course(calID, courseID)
        course_uuid = course.courseuuid
        if 'content' not in request_body and 'all' not in request_body and 'type' not in request_body:
            raise BadRequest
        if request_body['type'] not in MAIN_SLOT_TYPES:
            raise BadRequest
        if request_body['all'] == 'yes':
            SlotUtils.delete_all_slots(course_uuid, request_body['type'])
        else:
            content = request_body['content']
            for item in content:
                slot = ObjectChecks.check_slot_time_del(request_body['type'], item['time'], item['location'], item['type'], course_uuid)
                if slot is not None:
                    db.session.delete(slot)
            db.session.commit()

    def restore_all_original_slots(calID, courseID):
        check_cal(calID)
        course = check_course(calID, courseID)
        course_ID = course.courseID
        course_uuid = course.courseuuid
        delete_all_slots(course_uuid)
        add_all_slots(course_ID, course_uuid)
