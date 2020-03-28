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

    prevDept = request.cookies.get('prevDept')
    if prevDept is None:
        prevDept = ''

    prevNum = request.cookies.get('prevNum')
    if prevNum is None:
        prevNum = ''

    prevArea = request.cookies.get('prevArea')
    if prevArea is None:
        prevArea = ''

    prevTitle = request.cookies.get('prevTitle')
    if prevTitle is None:
        prevTitle = ''

    dept = request.args.get('dept')
    num = request.args.get('coursenum')
    area = request.args.get('area')
    title = request.args.get('title')
    query = {'-dept':dept,'-coursenum':num, '-area':area, '-title':title}

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
        num=num,
        area=area,
        title=title,
        entries=entries)

    response = make_response(html)
    response.set_cookie('prevDept', dept)
    response.set_cookie('prevAuthor', num)
    response.set_cookie('prevAuthor', area)
    response.set_cookie('prevAuthor', title)
    return response
   
#-----------------------------------------------------------------------

@app.route('/regdetails', methods=['GET'])
def regdetails():
    
    database = Database()
    database.connect()
    books = database.search(author)
    database.disconnect()
     
    html = render_template('searchresults.html',
        ampm=getAmPm(),
        currentTime=getCurrentTime(),
        author=author,
        books=books)
    response = make_response(html)
    response.set_cookie('prevAuthor', author)
    return response         
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
