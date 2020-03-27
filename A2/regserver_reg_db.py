#!/usr/bin/env python

#-------------------------------------------------------------
# regserver_reg_db.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
from re import compile

#-------------------------------------------------------------

BEGINNING = 'SELECT classid, dept, coursenum, area, title FROM classes, courses, crosslistings ' + \
	'WHERE classes.courseid = crosslistings.courseid AND classes.courseid = courses.courseid'
DEPT = " AND crosslistings.dept LIKE ?"
CRS_NUM = " AND crosslistings.coursenum LIKE ?"
AREA = " AND courses.area LIKE ?"
TITLE = " AND courses.title LIKE ? ESCAPE '\\'"
ORDER = ' ORDER BY dept, coursenum, classid ASC;'

#--------------------------------------------------------------------------------

def make_connection(database):
	if not path.isfile(database):
		return True, None, None
	connection = connect(database)
	cursor = connection.cursor()
	return False, connection, cursor

#--------------------------------------------------------------------------------

def produce_output(dictionary):
	stmtStr = BEGINNING
	vals = []
	for key,value in dictionary.items():
		value = value.replace('%', '\\%')
		value = value.replace('_', '\\_')
		value = value.lower()
		vals.append('%' + value + '%')
		if (key == '-dept'): stmtStr += DEPT
		elif (key == '-coursenum'): stmtStr += CRS_NUM
		elif (key == '-area'): stmtStr += AREA
		elif (key == '-title'): stmtStr += TITLE
	stmtStr += ORDER
	return stmtStr, vals

#--------------------------------------------------------------------------------

def get_output(cursor):
	entries = []
	row = cursor.fetchone()
	while row is not None:
		entries.append('{:>5}{:>5}{:>7}{:>5} {}'.format(row[0], row[1], row[2], row[3], row[4]))
		row = cursor.fetchone()
	return entries

#--------------------------------------------------------------------------------

def close(cursor, connection):
	cursor.close()
	connection.close()

#--------------------------------------------------------------------------------

def access_reg_db(dictionary):
	DATABASE = 'reg.sqlite'
	error, connection, cursor = make_connection(DATABASE)
	if error: 
		print('regserver: database %s not found' % DATABASE, file=stderr)
		return {'error': 'regserver: database %s not found' % DATABASE}

	try:
		instruction, vals = produce_output(dictionary)
		cursor.execute(instruction, vals)
		entries = {'success': get_output(cursor)}
	except Exception as e:
		print('regserver: ' + str(e), file=stderr)
		entries = {'error': 'regserver: ' + str(e)}

	close(cursor, connection)
	return entries



