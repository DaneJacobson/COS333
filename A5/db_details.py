#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_details.py
# Author: David Basili and Dane Jacobson
#-----------------------------------------------------------------------

from sys import stderr
from re import compile

#-------------------------------------------------------------
    
STR_LOC = 'SELECT courseid, days, starttime, endtime, bldg, roomnum FROM classes WHERE classid = ?;'
STR_DEPT = 'SELECT dept, coursenum FROM classes, crosslistings WHERE classes.courseid = crosslistings.courseid ' + \
                'AND classid = ? ORDER BY dept, coursenum ASC;'
STR_REQS = 'SELECT area, title, descrip, prereqs FROM classes, courses ' + \
                'WHERE classes.courseid = courses.courseid AND classid = ?;'
STR_PROF = 'SELECT profname FROM classes, coursesprofs, profs WHERE classes.courseid = coursesprofs.courseid ' + \
                'AND coursesprofs.profid = profs.profid AND classid = ? ORDER BY profname ASC;'

#-------------------------------------------------------------

def call_db(cursor, instruction, classid):
    cursor.execute(instruction, [classid])
    row = cursor.fetchone()
    if row is None and instruction == STR_LOC: 
        raise Exception("classid does not exist")
    return row

#-------------------------------------------------------------

def class_loc(cursor, classid):
    row = call_db(cursor, STR_LOC, classid)
    s0, s1, s2, s3, s4, s5 = str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])
    return {'course id': s0, 'days': s1, 'start time': s2, 'end time': s3, 'building': s4, 'room': s5}

#-------------------------------------------------------------

def dept(cursor, classid):
    row = call_db(cursor, STR_DEPT, classid)
    result = []
    while row is not None:
        result.append(str(row[0])+' '+str(row[1]))
        row = cursor.fetchone()
    return {'dept and number': result}

#-------------------------------------------------------------

def crs_reqs(cursor, classid):
    row = call_db(cursor, STR_REQS, classid)
    s0, s1, s2, s3 = str(row[0]), str(row[1]), str(row[2]), str(row[3])
    return {'area': s0, 'title': s1, 'description': s2, 'prerequisites': s3}

#-------------------------------------------------------------

def prof(cursor, classid):
    row = call_db(cursor, STR_PROF, classid)
    result = []
    while row is not None:
        result.append(str(row[0]))
        row = cursor.fetchone()
    return {'professor': result}

#-------------------------------------------------------------

def db_details(cursor, dictionary):
    try:
        classid = dictionary['classid']
        dictionary = class_loc(cursor, classid)
        dictionary = {**dictionary, **dept(cursor, classid)}
        dictionary = {**dictionary, **crs_reqs(cursor, classid)}
        dictionary = {**dictionary, **prof(cursor, classid)}
        info = {'success': dictionary}
    except Exception as e:
        print('database: ' + str(e), file=stderr)
        info = {'error': 'database: ' + str(e)}
    return info


