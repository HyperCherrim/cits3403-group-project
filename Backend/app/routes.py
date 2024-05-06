from flask import render_template
from app import app
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Debug User'}
    availableGroups = [{"unit":"CITS2200: Data Structures and Algorithms"}, 
                       {"unit":"CITS1003: Introduction to Cybersecurity"}, 
                       {"unit":"MATH1721: Mathematics Foundations: Methods"}] # Populate this later once options for new tags are added
    return render_template("index.html",title="Study Group maker",user=user,groups=availableGroups, cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/making_request')
def making_request():
    return render_template("making_request.html",title="making request",cssFile="../static/main.css",jsFile="../static/populateTable.js")

@app.route('/password_reset')
def password_reset():
    return render_template("password_reset.html",title="reset password",cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/responding_request')
def responding_request():
    return render_template("responding_request.html",title="respond to request",cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/user_creation')
def user_creation():
    return render_template("user_creation.html",title="account",cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/user_login')
def user_login():
    return render_template("user_login.html",title="login",cssFile="../static/main.css",jsFile="../static/main.js")