#!/usr/bin/env python

#-----------------------------------------------------------------------
# db_search.py
# Author: David Basili and Dane Jacobson
#-----------------------------------------------------------------------

from sys import stderr

#-----------------------------------------------------------------------

STR_INTRO = "SELECT classid, dept, coursenum, area, title FROM classes, courses, crosslistings " + \
            "WHERE classes.courseid = crosslistings.courseid AND classes.courseid = courses.courseid"
STR_DEPT = " AND crosslistings.dept LIKE ?"
STR_CRSNUM = " AND crosslistings.coursenum LIKE ?"
STR_AREA = " AND courses.area LIKE ?"
STR_TITLE = " AND courses.title LIKE ? ESCAPE '\\'"
STR_ORDER = " ORDER BY dept, coursenum, classid ASC;"

#-----------------------------------------------------------------------

def produce_output(dictionary):
    stmtStr = STR_INTRO
    vals = []
    for key,value in dictionary.items():
        if value is None: continue
        value = value.replace('%', '\\%')
        value = value.replace('_', '\\_')
        value = value.lower()
        vals.append('%' + value + '%')
        if (key == '-dept'): stmtStr += STR_DEPT
        elif (key == '-coursenum'): stmtStr += STR_CRSNUM
        elif (key == '-area'): stmtStr += STR_AREA
        elif (key == '-title'): stmtStr += STR_TITLE
    stmtStr += STR_ORDER
    return stmtStr, vals

#-----------------------------------------------------------------------

def get_output(cursor):
    entries = []
    row = cursor.fetchone()
    while row is not None:
        entries.append({'classid': str(row[0]), 'dept': row[1], 'coursenum': str(row[2]), 'area': row[3], 'title': row[4]})
        # entries.append('{:>5}{:>5}{:>7}{:>5} {}'.format(row[0], row[1], row[2], row[3], row[4]))
        row = cursor.fetchone()
    return entries

#-----------------------------------------------------------------------

def db_search(cursor, dictionary):
    try:
        instruction, vals = produce_output(dictionary)
        cursor.execute(instruction, vals)
        entries = {'success': get_output(cursor)}
    except Exception as e:
        print('database: ' + str(e), file=stderr)
        entries = {'error': 'database: ' + str(e)}
    return entries
