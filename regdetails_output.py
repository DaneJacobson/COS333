#!/usr/bin/env python

#-------------------------------------------------------------
# reg_output.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
from re import compile
from regdetails_check import report_err

#-------------------------------------------------------------

CLASS_LOC = 'SELECT courseid, days, starttime, endtime, bldg, roomnum FROM classes WHERE classid = ?;'
DEPT = 'SELECT dept, coursenum FROM classes, crosslistings WHERE classes.courseid = crosslistings.courseid ' + \
'AND classid = ? ORDER BY dept, coursenum ASC;'
CRS_REQS = 'SELECT area, title, descrip, prereqs FROM classes, courses ' + \
'WHERE classes.courseid = courses.courseid AND classid = ?;'
PROF = 'SELECT profname FROM classes, coursesprofs, profs WHERE classes.courseid = coursesprofs.courseid ' + \
'AND coursesprofs.profid = profs.profid AND classid = ? ORDER BY profname ASC;'

#--------------------------------------------------------------------------------

def make_connection(database):
	if not path.isfile(database):
		report_err("database reg.sqlite not found")
	connection = connect(database)
	cursor = connection.cursor()
	return connection, cursor

#--------------------------------------------------------------------------------

def norm(line):
	CHARS_PER_LINE = 72

	result, outline = '', ''
	re_word = compile(r'\S+')
	words = re_word.findall(line)
	for word in words:
		if len(outline) + len(word) > CHARS_PER_LINE:
			result += outline.rstrip() + '\n'
			outline = ''
		outline += word + ' '
	if outline:
		result += outline.rstrip()
	return result

#--------------------------------------------------------------------------------

def call_db(cursor, instruction, classid):
	cursor.execute(instruction, [classid])
	row = cursor.fetchone()
	if row is None: report_err('classid does not exist')
	return row

#--------------------------------------------------------------------------------

def print_lines(lines):
	for line in lines:
		print(line)

#--------------------------------------------------------------------------------

def class_loc(cursor, classid, h):
	row = call_db(cursor, CLASS_LOC, classid)
	s0, s1, s2, s3, s4, s5 = str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])
	if h: 
		s0 = norm('Course Id: %s' % s0) + '\n'
		s1 = norm('Days: %s' % s1)
		s2 = norm('Start time: %s' % s2)
		s3 = norm('End time: %s' % s3)
		s4 = norm('Building: %s' % s4)
		s5 = norm('Room: %s' % s5) + '\n'
	print_lines([s0, s1, s2, s3, s4, s5])

#--------------------------------------------------------------------------------

def dept(cursor, classid, h):
	msg = '{} {}' if not h else 'Dept and Number: {} {}'
	row = call_db(cursor, DEPT, classid)
	while row is not None:
		print(msg.format(str(row[0]), str(row[1])))
		row = cursor.fetchone()
	if h: print()

#--------------------------------------------------------------------------------

def crs_reqs(cursor, classid, h):
	row = call_db(cursor, CRS_REQS, classid)
	s0, s1, s2, s3 = str(row[0]), str(row[1]), str(row[2]), str(row[3])
	if h:
		s0 = norm('Area: %s' % s0) + '\n'
		s1 = norm('Title: %s' % s1) + '\n'
		s2 = norm('Description: %s' % s2) + '\n'
		s3 = norm('Prerequisites: %s' % s3) + '\n'
	print_lines([s0, s1, s2, s3])

#--------------------------------------------------------------------------------

def prof(cursor, classid, h):
	msg = '{}' if not h else 'Professor: {}'
	row = call_db(cursor, PROF, classid)
	while row is not None:
		print(msg.format(str(row[0])))
		row = cursor.fetchone()

#--------------------------------------------------------------------------------

def close(cursor, connection):
	cursor.close()
	connection.close()

#--------------------------------------------------------------------------------

def execute_output(classid, h, database):
	connection, cursor = make_connection(database)
	try:
		class_loc(cursor, classid, h)
		dept(cursor, classid, h)
		crs_reqs(cursor, classid, h)
		prof(cursor, classid, h)
	except Exception as e:
		print('regdetails: ' + str(e), file=stderr)
		close(cursor, connection)
		exit(1)
	close(cursor, connection)


	
