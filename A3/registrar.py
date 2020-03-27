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
    
    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    prevDept = request.cookies.get('prevDept')
    if prevDept is None:
        prevDept = '(None)'

    prevNum = request.cookies.get('prevNum')
    if prevNum is None:
        prevNum = '(None)'

    prevArea = request.cookies.get('prevArea')
    if prevArea is None:
        prevArea = '(None)'

    prevTitle = request.cookies.get('prevTitle')
    if prevTitle is None:
        prevTitle = '(None)'

    # dept = request.args.get('dept')
    # num = request.args.get('coursenum')
    # area = request.args.get('area')
    # title = request.args.get('title')

    #query = {'-dept':dept,'-coursenum':coursenum, '-area':area, '-title':title}
    query = {}

    database = Database()
    entries = database.search(query)
    print(entries)
    formatted_txt = []
    for entry in entries['success']:
        formatted_txt.append('{:>5}{:>5}{:>7}{:>5} {}'.format(entry['classid'], entry['dept'], entry['coursenum'], entry['area'], entry['title']))

    entries = entries.get('success')
    html = render_template('index.html',
        entries=entries)
    response = make_response(html)
    return response
   
#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def classdetails():
    
    author = request.args.get('author')
    if (author is None) or (author.strip() == ''):
        errorMsg = 'Please type an author name.'
        return redirect(url_for('searchForm', errorMsg=errorMsg))
 
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
