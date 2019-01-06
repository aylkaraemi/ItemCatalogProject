#!/usr/bin/env python3
from flask import (
    Flask, render_template, request, redirect,
    jsonify, url_for, flash, make_response, g)
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, Book
import random
import string

CLIENT_ID = json.loads(open('client_secrets.json').read())['web']['client_id']

baseURL = 'https://www.googleapis.com/oauth2/v1/'

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///readinglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', clientID=CLIENT_ID, state=state)


@app.route('/gconnect', methods=['POST'])
def googleConnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('State parameter is invalid.'), 401)
        response.headers['content-type'] = 'application/json'
        return response

    auth_code = request.data
    try:
        oauthFlow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauthFlow.redirect_uri = 'postmessage'
        credentials = oauthFlow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            "There was a problem exchanging credentials."), 401)
        response.headers['content-type'] = 'application/json'
        return response

    accessToken = credentials.access_token
    validationURL = baseURL + 'tokeninfo?access_token={}'.format(
        accessToken)
    h = httplib2.Http()
    result = json.loads(h.request(validationURL, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    googleID = credentials.id_token['sub']
    if result['user_id'] != googleID:
        response = make_response(
            json.dumps("Token is not valid for user."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token is not valid for this app."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    storedToken = login_session.get('accessToken')
    storedGoogleID = login_session.get('googleID')
    if storedToken is not None and googleID == storedGoogleID:
        response = make_response(json.dumps("You are already logged in."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['accessToken'] = accessToken
    login_session['googleID'] = googleID

    userinfoURL = baseURL + 'userinfo'
    params = {'access_token': accessToken, 'alt': 'json'}
    answer = requests.get(userinfoURL, params=params)
    userInfo = answer.json()

    login_session['username'] = userInfo['name']
    login_session['email'] = userInfo['email']

    user = session.query(User).filter_by(
        email=login_session['email']).first()
    if not user:
        newUser = User(
            name=login_session['username'], email=login_session['email'])
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(
            email=login_session['email']).first()
    login_session['userID'] = user.id
    output = '<h1>Welcome {}!</h1>'.format(login_session['username'])
    return output


@app.route('/disconnect')
def disconnect():
    accessToken = login_session.get('accessToken')
    if accessToken is None:
        response = make_response(json.dumps('User is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(
        accessToken)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['accessToken']
        del login_session['googleID']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('You are now logged off'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Disconnect failed.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/readinglist/JSON')
def readingListJSON():
    return "This will be a JSON endpoint"


@app.route('/')
@app.route('/readinglist')
def viewReadingList():
    sampleuser = session.query(User).filter_by(name="SampleUser").first()
    books = session.query(Book).filter_by(user_id=sampleuser.id).all()
    return render_template('publiclist.html', books=books)


@app.route('/readinglist/<string:genre>')
def viewGenre(genre):
    sampleuser = session.query(User).filter_by(name="SampleUser").first()
    books = session.query(Book).filter_by(
        user_id=sampleuser.id, genre=genre).all()
    return render_template('publicgenrelist.html', genre=genre, books=books)


@app.route('/readinglist/<int:id>')
def viewBook(id):
    book = session.query(Book).filter_by(id=id).first()
    return render_template('publicbook.html', book=book)


@app.route('/readinglist/add', methods=['GET', 'POST'])
def addBook():
    return render_template('addbook.html')


@app.route('/readinglist/<int:id>/edit', methods=['GET', 'POST'])
def editBook(id):
    return render_template('editbook.html')


@app.route('/readinglist/<int:id>/delete', methods=['GET', 'POST'])
def deleteBook(id):
    return render_template('deletebook.html')


if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
