from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login
import sqlalchemy as alchemy
from app.models import Users, Groups
from app.forms import userLogin, userRegister, initialiseGroup
from dateConversion import encodeTimes
import json
@app.route('/')
@app.route('/index')
def index():
    availableGroups = Groups.query.all()
    user = Users.query.all()
    units = db.session.query(Groups.tagOne).order_by(alchemy.desc(Groups.tagOne)).all()
    return render_template("index.html",title="Study Group Organiser Application",user=user,groups=availableGroups,cssFile="../static/main.css",jsFile="../static/main.js", units=units)

@app.route('/createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    newGroup = initialiseGroup()
    if newGroup.validate_on_submit():
        dateTimes = [newGroup.availStart.data, newGroup.availEnd.data]
        processedTimes = encodeTimes(dateTimes)
        username = db.session.query(Users.userID).where(current_user.userName == Users.userName)
        resultantList = json.dumps(processedTimes)
        addGroup = Groups(userID=username, groupName=newGroup.groupTitle.data, tagOne=newGroup.tagOne.data, tagTwo=newGroup.tagTwo.data, tagThree=newGroup.tagThree.data, groupDescription=newGroup.groupDesc.data, studentAvailability=resultantList, requiredStudents=newGroup.requiredStudents.data)
        db.session.add(addGroup)
        db.session.commit()
        flash("Group creation successful! ")
        return redirect(url_for('index'))
    return render_template("newGroupSubmit.html",title="Create a Group - Study Group Organiser", form=newGroup)

@app.route('/password_reset')
@login_required
def password_reset():
    return render_template("password_reset.html",title="Reset Password",cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/responding_request')
@login_required
def responding_request():
    return render_template("responding_request.html",title="Reply to Group Request",cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/user_creation', methods=['GET', 'POST'])
def user_creation():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    regform = userRegister()
    if regform.validate_on_submit():
        user = Users(fullName=regform.studentFN.data, userName=regform.studentUN.data, userEmail=regform.studentEM.data)
        user.setPassword(regform.studentPW.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for('user_login'))
    return render_template("user_creation.html",title="Register Account - Study Group Organiser",form=regform,cssFile="../static/main.css",jsFile="../static/main.js")

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    form = userLogin()
    if form.validate_on_submit() == True:
        user = db.session.scalar(alchemy.select(Users).where(Users.userName == form.studentUser.data))
        if user is None or not user.getPassword(form.studentPwd.data):
            flash("Invalid login details")
            return redirect(url_for('user_login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template("user_login.html",title="Log In - Study Group Organiser",form=form,cssFile="../static/main.css",jsFile="../static/main.js")
@app.route('/logout')
@login_required
def userLogout():
    logout_user()
    return(redirect(url_for('index')))

@login.user_loader
def getID(userID):
    return db.session.get(Users, int(userID))

@app.errorhandler(401)
def unauthorisedError(error):
    flash("You are not signed in!")
    return redirect(url_for("user_login"))
