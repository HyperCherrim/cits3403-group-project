from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login
import sqlalchemy as alchemy

from app.models import Users, Groups, TimeSlot
from app.forms import userLogin, userRegister, submitTimes, TimeSlotForm, WeekForm, replyForm
from datetime import time

@app.route('/')
@app.route('/index')
def index():
    availableGroups = Groups.query.all()
    user = Users.query.all()
    units = db.session.query(Groups.tagOne).order_by(alchemy.desc(Groups.tagOne)).all()
    return render_template("index.html",title="Study Group Organiser Application",user=user,groups=availableGroups,cssFile="../static/main.css",jsFile="../static/main.js", units=units)

@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    form = WeekForm()
    print("hello 1")
    if form.validate_on_submit():
        print("hello 1")
        # Create and save the Group instance
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
        print("User ID: {}".format(loggedInUserID))
        # Save the TimeSlot instances
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            for slot in getattr(form, day).entries:
                start_time = time.fromisoformat(slot.start_time.data)
                end_time = time.fromisoformat(slot.end_time.data)
                print(start_time)
                print(start_time >= end_time)
                if not start_time == end_time:
                    if start_time > end_time:
                        flash(f'End time must be after start time for {day.capitalize()}.', 'danger')
                        return render_template('createGroup.html', form=form)
        group = Groups(
            userID=loggedInUserID,  # This should be dynamically set, e.g., from the logged-in user
            groupTitle=form.groupTitle.data,
            tagOne=form.groupTag1.data,
            tagTwo=form.groupTag2.data,
            tagThree=form.groupTag3.data,
            description=form.description.data,
            requiredStudents=form.requiredStudents.data
        )
        db.session.add(group)
        db.session.commit()

        # Save the TimeSlot instances
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            for slot in getattr(form, day).entries:
                start_time = time.fromisoformat(slot.start_time.data)
                end_time = time.fromisoformat(slot.end_time.data)
                print(start_time)
                print(start_time >= end_time)
                if not start_time == end_time:
                    if start_time > end_time:
                        flash(f'End time must be after start time for {day.capitalize()}.', 'danger')
                        return render_template('createGroup.html', form=form)
                    new_slot = TimeSlot(
                        userID=loggedInUserID,
                        groupID=group.groupID,
                        day=day,
                        start_time=start_time,
                        end_time=end_time
                    )
                    db.session.add(new_slot)
            db.session.commit()
        flash('Time slots and group saved!', 'success')
        return redirect(url_for('index'))
    return render_template("createGroup.html",title="Create a Group - Study Group Organiser",cssFile="../static/main.css",jsFile="../static/populateTable.js", form=form)


@app.route('/submitReply/<int:groupID>')
@login_required
def submitResponse(groupID):
    print("Do you hear me?")
    respondingForm = replyForm()
    
    return render_template("submitResponse.html",title="Apply to Join Group",cssFile="../static/responding_request.css",jsFile="../static/main.js", form=respondingForm, groupID=groupID)

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
        if user is None or not user.getPassword(form.studentPwd.data):
            flash("Invalid login details")
            return redirect(url_for('user_login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template("user_login.html",title="Log In - Study Group Organiser",form=form,cssFile="../static/login.css",jsFile="../static/main.js")

@app.route('/logout')
@login_required
def userLogout():
    logout_user()
    return(redirect(url_for('index')))

@app.route('/user')
@login_required
def user_page():
    username = current_user.userName
    groups = Groups.query.all()

    notifications = [{"Title":"CITS:2200 exam", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"Book club", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"team all the marks", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"Example Title4", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     ]
    # groups = []
    # notifications = []


    return render_template("user_page.html",title=username, user=username, groups=groups, cssFile="../static/userpage.css" ,notifications=notifications)



@login.user_loader
def getID(userID):
    return db.session.get(Users, int(userID))

@app.errorhandler(401)
def unauthorisedError(error):
    flash("You are not signed in!")
    return redirect(url_for("user_login"))
