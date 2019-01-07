#!/usr/bin/env python3
from flask import (
    Flask, render_template, request, redirect,
    jsonify, url_for, flash, make_response)
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Book
import random
import string

CLIENT_ID = json.loads(open('client_secrets.json').read())['web']['client_id']

baseURL = 'https://www.googleapis.com/oauth2/v1/'

app = Flask(__name__)

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
    # match state tokens to confirm request is valid
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('State parameter is invalid.'), 401)
        response.headers['content-type'] = 'application/json'
        return response
    # attempt to exchange auth code for token
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
    # check if token is valid with google API server
    accessToken = credentials.access_token
    validationURL = baseURL + 'tokeninfo?access_token={}'.format(
        accessToken)
    h = httplib2.Http()
    result = json.loads(h.request(validationURL, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # if token is valid, confirm token is valid for user
    googleID = credentials.id_token['sub']
    if result['user_id'] != googleID:
        response = make_response(
            json.dumps("Token is not valid for user."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # if token is valid and valid for user, confirm is valid for app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token is not valid for this app."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # if token is valid in every way, confirm if user is already logged in
    storedToken = login_session.get('accessToken')
    storedGoogleID = login_session.get('googleID')
    if storedToken is not None and googleID == storedGoogleID:
        response = make_response(json.dumps("You are already logged in."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # if user is not already logged in store token & googleID
    login_session['accessToken'] = accessToken
    login_session['googleID'] = googleID
    # get user info from google API server
    userinfoURL = baseURL + 'userinfo'
    params = {'access_token': accessToken, 'alt': 'json'}
    answer = requests.get(userinfoURL, params=params)
    userInfo = answer.json()
    # save username and email of user in login_session
    login_session['username'] = userInfo['name']
    login_session['email'] = userInfo['email']
    # check if there is record for user in database, if not add user
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
    flash('Welcome {}!'.format(login_session['username']))
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
        flash('You have successfully logged off.')
        return redirect(url_for('viewReadingList'))
    else:
        response = make_response(json.dumps('Disconnect failed.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/readinglist/JSON')
def readingListJSON():
    books = session.query(Book).all()
    return jsonify(books=[book.serialize for book in books])


@app.route('/readinglist/<string:genre>/JSON')
def genreListJSON(genre):
    books = session.query(Book).filter_by(genre=genre).all()
    if books:
        return jsonify(books=[book.serialize for book in books])
    else:
        return jsonify({'error': 'No books found for {}'.format(genre)})


@app.route('/readinglist/<int:id>/JSON')
def bookJSON(id):
    book = session.query(Book).first()
    if book:
        return jsonify(book=book.serialize)


@app.route('/')
@app.route('/readinglist/')
def viewReadingList():
    if 'username' not in login_session:
        sampleuser = session.query(User).filter_by(name="SampleUser").first()
        books = session.query(Book).filter_by(user_id=sampleuser.id).all()
        return render_template('publiclist.html', books=books)
    else:
        user = session.query(User).filter_by(
            name=login_session['username']).first()
        books = session.query(Book).filter_by(user_id=user.id).all()
        return render_template('readinglist.html', books=books, name=user.name)


@app.route('/readinglist/<string:genre>')
def viewGenre(genre):
    if 'username' not in login_session:
        sampleuser = session.query(User).filter_by(name="SampleUser").first()
        books = session.query(Book).filter_by(
            user_id=sampleuser.id, genre=genre).all()
        return render_template(
            'publicgenrelist.html', genre=genre, books=books)
    else:
        user = session.query(User).filter_by(
            name=login_session['username']).first()
        books = session.query(Book).filter_by(
            user_id=user.id, genre=genre).all()
        return render_template('genrelist.html', books=books, name=user.name)


@app.route('/readinglist/<int:id>')
def viewBook(id):
    sampleuser = session.query(User).filter_by(name="SampleUser").first()
    book = session.query(Book).filter_by(id=id).first()
    if not book:
        flash('Requested book was not found.')
        return redirect(url_for('viewReadingList'))
    if book.user_id == sampleuser.id:
        return render_template('publicbook.html', book=book)
    elif 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        user = session.query(User).filter_by(
            name=login_session['username']).first()
        if book.user_id == user.id:
            return render_template('book.html', book=book, name=user.name)
        else:
            flash("""
                The book you are trying to access belongs to another user.
                Users only have access to the books on their own list and
                 the sample books.
                """)
            return redirect(url_for('viewReadingList'))


@app.route('/readinglist/add', methods=['GET', 'POST'])
def addBook():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(
        name=login_session['username']).first()
    if request.method == 'POST':
        newBook = Book(
            title=request.form['title'],
            author=request.form['author'],
            genre=request.form['genre'],
            description=request.form['description'],
            user_id=user.id)
        session.add(newBook)
        session.commit()
        flash('{} successfully added!'.format(newBook.title))
        return redirect(url_for('viewReadingList'))
    else:
        return render_template('addbook.html', name=user.name)


@app.route('/readinglist/<int:id>/edit', methods=['GET', 'POST'])
def editBook(id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(
        name=login_session['username']).first()
    book = session.query(Book).filter_by(id=id).first()
    if not book:
        flash('Requested book was not found.')
        return redirect(url_for('viewReadingList'))
    if book.user_id != user.id:
        flash("""
            {} (id: {}) belongs to another user.
            Users can only edit the books on their own list.
            """.format(book.title, book.id))
        return redirect(url_for('viewReadingList'))
    if request.method == 'POST':
        if request.form['title']:
            book.title = request.form['title']
        if request.form['author']:
            book.author = request.form['author']
        if request.form.get('genre'):
            book.genre = request.form.get('genre')
        if request.form['description']:
            book.description = request.form['description']
        session.add(book)
        session.commit()
        flash('{} succesfully updated.'.format(book.title))
        return redirect(url_for('viewReadingList'))
    else:
        return render_template('editbook.html', book=book, name=user.name)


@app.route('/readinglist/<int:id>/delete', methods=['GET', 'POST'])
def deleteBook(id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(
        name=login_session['username']).first()
    book = session.query(Book).filter_by(id=id).first()
    if not book:
        flash('Requested book was not found.')
        return redirect(url_for('viewReadingList'))
    if book.user_id != user.id:
        flash("""
            {} (id: {}) belongs to another user.
            Users can only delete the books on their own list.
            """.format(book.title, book.id))
        return redirect(url_for('viewReadingList'))
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash("Book successfully deleted.")
        return redirect(url_for('viewReadingList'))
    else:
        return render_template('deletebook.html', book=book, name=user.name)


if __name__ == '__main__':
    app.secret_key = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
