from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import app, db
import sqlalchemy as alchemy
from app.models import Users, Groups, ReplyMessages
from app.forms import userLogin, userRegister, submitTimes
@app.route('/')
@app.route('/index')
def index():
    availableGroups = Groups.query.all()
    user = Users.query.all()
    #user = {'username': 'Debug User'} # Since the user query is being weird, going back to the debug dictionary
    #availableGroups = [{"unit":"CITS2200: Data Structures and Algorithms"}, 
                       #{"unit":"CITS1003: Introduction to Cybersecurity"}, 
                       #{"unit":"MATH1721: Mathematics Foundations: Methods"}] # Populate this later once options for new tags are added
    return render_template("index.html",title="Study Group Organiser Application",user=user,groups=availableGroups,cssFile="../static/index.css",jsFile="../static/main.js")

@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    form = submitTimes()
    if form.validate_on_submit():
        groups = Groups(groupTitle=form.groupTitle.data, 
                        groupTag1=form.groupTag1.data, 
                        groupTag2=form.groupTag2.data, 
                        groupTag3=form.groupTag3.data, 
                        Description=form.Description.data, 
                        groupRequestSubmition=form.groupRequestSubmition.data, 
                        mondayStartTime=form.mondayStartTime.data, 
                        mondayEndTime=form.mondayEndTime.data, 
                        tuesdayStartTime=form.tuesdayStartTime.data, 
                        tuesdayEndTime=form.tuesdayEndTime.data, 
                        webnesdayStartTime=form.webnesdayStartTime.data, 
                        webnesdayEndTime=form.webnesdayEndTime.data, 
                        thursdayStartTime=form.thursdayStartTime.data, 
                        thursdayEndTime=form.thursdayEndTime.data, 
                        fridayStartTime=form.fridayStartTime.data, 
                        fridayEndTime=form.fridayEndTime.data, 
                        saterdayStartTime=form.saterdayStartTime.data, 
                        saterdayEndTime=form.saterdayEndTime.data, 
                        sundayStartTime=form.sundayStartTime.data, 
                        sundayEndTime=form.sundayEndTime.data)
        db.session.add(groups)
        db.session.commit()
        flash("group registration successful!")
        return redirect(url_for('index'))
    return render_template("createGroup.html",title="Create a Group - Study Group Organiser",cssFile="../static/main.css",jsFile="../static/populateTable.js", form=form)

@app.route('/password_reset')
def password_reset():
    return render_template("password_reset.html",title="Reset Password",cssFile="../static/password_reset.css",jsFile="../static/main.js")

@app.route('/responding_request')
def responding_request():
    return render_template("responding_request.html",title="Reply to Group Request",cssFile="../static/responding_request.css",jsFile="../static/main.js")

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
    return render_template("user_creation.html",title="Register Account - Study Group Organiser",form=regform,cssFile="../static/user_creation.css",jsFile="../static/main.js")

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    form = userLogin()
    if form.validate_on_submit() == True:
        user = db.session.scalar(alchemy.select(Users).where(Users.userName == form.studentUser.data))
        if user == None or not user.getPassword(form.studentPwd.data):
            flash("Invalid login details")
        login_user(user)
        return redirect(url_for('index'))
    return render_template("user_login.html",title="Log In - Study Group Organiser",form=form,cssFile="../static/login.css",jsFile="../static/main.js")

@app.route('/logout')
def userLogout():
    logout_user()
    return(redirect(url_for('index')))