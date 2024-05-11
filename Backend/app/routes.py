from flask import render_template
from flask_login import current_user, login_user
from app import app
#@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Debug User'}
    availableGroups = [{"unit":"CITS2200: Data Structures and Algorithms"}, 
                       {"unit":"CITS1003: Introduction to Cybersecurity"}, 
                       {"unit":"MATH1721: Mathematics Foundations: Methods"}] # Populate this later once options for new tags are added
    return render_template("index.html",title="Study Group maker",user=user,groups=availableGroups)

@app.route('/making_request')
def making_request():
    return render_template("making_request.html",title="making request")

@app.route('/password_reset')
def password_reset():
    return render_template("password_reset.html",title="reset password")

@app.route('/responding_request')
def responding_request():
    return render_template("responding_request.html",title="respond to request")

@app.route('/user_creation')
def user_creation():
    return render_template("user_creation.html",title="account")

@app.route('/user_login')
def user_login():
    return render_template("user_login.html",title="login")

@app.route('/')
@app.route('/user/<username>')
#@login_required
def user_page(username = "TEST"):
    user = "TEMPORARY"
    groups = ["group name 1",
              "group name 2",
              "group name 3"
             ]

    notifications = [{"Title":"Example Title1", "date":"29th", "time":"0800 - 0900","emails":["email","email"]},
                     {"Title":"Example Title2", "date":"30th", "time":"0930 - 1100","emails":["email","email"]},
                     {"Title":"Example Title3", "date":"31th", "time":"2200 - 2345","emails":["email","email"]},
                     {"Title":"Example Title4", "date":" 1st", "time":"0000 - 0100","emails":["email","email"]},
                     ]
    
    return render_template("user_page.html",title = user , user=user , groups=groups , cssFile="../static/userpage.css" , notifications = notifications)

