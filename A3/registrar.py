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

    dept = request.args.get('dept')
    coursenum = request.args.get('coursenum')
    area = request.args.get('area')
    title = request.args.get('title')

    if dept is None:
        dept = ''
    if coursenum is None:
        coursenum = ''
    if area is None:
        area = ''
    if title is None:
        title = ''

    query = {'-dept':dept,'-coursenum':coursenum, '-area':area, '-title':title}

    database = Database()
    entries = database.search(query)

    if 'error' in entries:
        return redirect(url_for('error', errorMsg=entries.get('error')))
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
    
    dept = request.cookies.get('dept')
    coursenum = request.cookies.get('coursenum')
    area = request.cookies.get('area')
    title = request.cookies.get('title')

    classid = request.args.get('classid')
    classid_query = {'classid':classid}

    database = Database()
    details = database.get_details(classid_query)

    if 'error' in details:
        return redirect(url_for('error', errorMsg=details.get('error')))
    details = details.get('success')

    html = render_template('regdetails.html',
        classid=classid,
        dept=dept,
        coursenum=coursenum,
        area=area,
        title=title,
        details=details)
    response = make_response(html)
    return response         
    
#-----------------------------------------------------------------------

@app.route('/error')
def error():

    html = render_template('error.html', 
        errorMsg=request.args.get('errorMsg'))
    response = make_response(html)
    return response  

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
