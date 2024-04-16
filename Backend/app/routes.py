from flask import render_template
from app import app
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template("index.html",title="Study Group maker",user=user)

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