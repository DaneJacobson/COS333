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
@app.route('/search', methods=['GET'])
def index():

    html = render_template('index.html')
    response = make_response(html)
    return response


#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search():

    # generate search query
    dept = request.args.get('department')
    coursenum = request.args.get('number')
    area = request.args.get('area')
    title = request.args.get('title')

    # if this is the first page load, set fields to ''
    if (dept is None) or (dept.strip() == ''): dept = ''
    if (coursenum is None) or (coursenum.strip() == ''): coursenum = ''
    if (area is None) or (area.strip() == ''): area = ''
    if (title is None) or (title.strip() == ''): title = ''

    # build query and perform search
    query = {'-dept':dept,'-coursenum':coursenum, '-area':area, '-title':title}
    database = Database()
    entries = database.search(query)

    # error handling, create entries for template
    if 'error' in entries:
        return redirect(url_for('error', errorMsg=entries.get('error')))
    entries = entries.get('success')

    # return html for table of classes
    html = render_template('searchresults.html',entries=entries)
    response = make_response(html)
    return response
   
#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def regdetails():
    
    # build details query and perform search
    classid_query = {'classid':classid}
    database = Database()
    details = database.get_details(classid_query)

    # error handling, create details for template
    if 'error' in details:
        return redirect(url_for('error', errorMsg=details.get('error')))
    details = details.get('success')

    # render regdetails.html, and return
    html = render_template('regdetails.html',
        classid=classid,
        details=details)
    response = make_response(html)
    return response         
    
#-----------------------------------------------------------------------

@app.route('/error')
def error():

    # render error.html with application-specific message, and return
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
