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

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///readinglist.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    return render_template('login.html')


@app.route('/readinglist/JSON')
def readingListJSON():
    return "This will be a JSON endpoint"


@app.route('/')
@app.route('/readinglist')
def viewReadingList():
    return render_template('publiclist.html')


@app.route('/readinglist/<string:genre>')
def viewGenre(genre):
    return render_template('publicgenrelist.html', genre=genre)


@app.route('/readinglist/<int:id>')
def viewBook(id):
    return render_template('publicbook.html')


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
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
