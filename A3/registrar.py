#!/usr/bin/env bash

#-----------------------------------------------------------------------
# registrar.py
# Author: David Basili and Dane Jacobson
#-----------------------------------------------------------------------

from sys import argv, stderr
from database import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    # prevDept = request.cookies.get('prevDept')
    # if prevDept is None:
    #     prevDept = ''

    # prevNum = request.cookies.get('prevNum')
    # if prevNum is None:
    #     prevNum = ''

    # prevArea = request.cookies.get('prevArea')
    # if prevArea is None:
    #     prevArea = ''

    # prevTitle = request.cookies.get('prevTitle')
    # if prevTitle is None:
    #     prevTitle = ''

    # dept = request.args.get('dept')
    # num = request.args.get('coursenum')
    # area = request.args.get('area')
    # title = request.args.get('title')

    dept = request.args.get('dept')
    if dept is '':
        dept = request.cookies.get('dept')
    if dept is None:
        dept = ''

    coursenum = request.args.get('coursenum')
    if coursenum is '':
        coursenum = request.cookies.get('coursenum')
    if coursenum is None:
        coursenum = ''

    area = request.args.get('area')
    if area is '':
        area = request.cookies.get('area')
    if area is None:
        area = ''

    title = request.args.get('title')
    if title is '':
        title = request.cookies.get('title')
    if title is None:
        title = ''

    query = {'-dept':dept,'-coursenum':coursenum, '-area':area, '-title':title}

    database = Database()
    entries = database.search(query)
    
    # if dept is None:
    #     dept = ''
    # if num is None:
    #     num = ''
    # if area is None:
    #     area = ''
    # if title is None:
    #     title = ''

    entries = entries.get('success')
    html = render_template('index.html',
        dept=dept,
        coursenum=coursenum,
        area=area,
        title=title,
        entries=entries)

    response = make_response(html)
    response.set_cookie('dept', dept)
    response.set_cookie('coursenum', coursenum)
    response.set_cookie('area', area)
    response.set_cookie('title', title)
    return response
   
#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def regdetails():
    
    classid = request.args.get('classid')
    classid_query = {'classid':classid}

    database = Database()
    details = database.get_details(classid_query)

    details = details.get('success')
    html = render_template('regdetails.html',
        classid=classid,
        details=details)
    response = make_response(html)
    return response         
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
