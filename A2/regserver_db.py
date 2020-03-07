#!/usr/bin/env python

#-------------------------------------------------------------
# regserver_db.py
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

def get_title(title):
	CHARS_PER_LINE = 72 - 23

	result, outline = '', ''
	re_word = compile(r'\S+')
	words = re_word.findall(title)
	for word in words:
		if len(outline) + len(word) > CHARS_PER_LINE:
			result += outline.rstrip() + '\n                       '
			outline = ''
		outline += word + ' '
	if outline:
		result += outline.rstrip()
	return result

#--------------------------------------------------------------------------------

def get_output(cursor):
	entries = {}
	row = cursor.fetchone()
	while row is not None:
		classid, dept, crsnm, area = row[0], row[1], row[2], row[3]
		title = get_title(row[4])
		entries[classid] = '{:>5}{:>5}{:>7}{:>5} {}'.format(classid, dept, crsnm, area, title)
		row = cursor.fetchone()
	return entries

#--------------------------------------------------------------------------------

def close(cursor, connection):
	cursor.close()
	connection.close()

#--------------------------------------------------------------------------------

def access_db(dictionary):
	DATABASE = 'reg.sqlite'
	error, connection, cursor = make_connection(DATABASE)
	if error: return {'error': 'database reg.sqlite not found'}

	try:
		instruction, vals = produce_output(dictionary)
		cursor.execute(instruction, vals)
		entries = get_output(cursor)
	except Exception as e:
		print('regserver: ' + str(e), file=stderr)
		entries = {'error': str(e)}

	close(cursor, connection)
	return entries



