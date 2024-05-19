
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login
import sqlalchemy as alchemy
from TimeLineUp import CheckOverlap

from app.models import Users, Groups, TimeSlot, ReplyMessages
from app.forms import userLogin, userRegister, submitTimes, TimeSlotForm, WeekForm, replyForm
from datetime import time as TimeDay

@app.route('/')
@app.route('/index')
def index():
    availableGroups = Groups.query.all()
    user = Users.query.all()
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    units = db.session.query(Groups.tagOne).order_by(alchemy.desc(Groups.tagOne)).all()
    return render_template("index.html",title="Study Group Organiser Application",user=user,groups=availableGroups,cssFile="../static/index.css",jsFile="../static/main.js", units=units,userID = loggedInUserID)

@login_required
@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    else:
        return redirect(url_for('user_login'))
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

                        return render_template('createGroup.html', form=form,userID = loggedInUserID)
        groupList = []
        groupList.append(str(loggedInUserID))
        groupStr = "---".join(groupList)

        group = Groups(
            userID=loggedInUserID,  # This should be dynamically set, e.g., from the logged-in user
            groupTitle=form.groupTitle.data,
            tagOne=form.groupTag1.data,
            tagTwo=form.groupTag2.data,
            tagThree=form.groupTag3.data,
            description=form.description.data,
            requiredStudents=form.requiredStudents.data,
            members=groupStr,
            numberOfHours=form.requiredStudents.data
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
                        return render_template('createGroup.html', form=form,userID = loggedInUserID)
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
    return render_template("createGroup.html",title="Create a Group - Study Group Organiser",cssFile="../static/createGroup.css",jsFile="../static/populateTable.js", form=form,userID = loggedInUserID)

@app.route('/password_reset')
def password_reset():
    return render_template("password_reset.html",title="Reset Password",cssFile="../static/password_reset.css",jsFile="../static/main.js")

@app.route('/submitResponse/<int:groupID>', methods=["GET", "POST"])
@login_required
def submitResponse(groupID):

    loggedInUserID = db.session.scalar(
        alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    groupObj = db.session.scalar(alchemy.select(Groups).where(Groups.groupID == groupID))
    respondingForm = replyForm()

    # Fetch available time ranges for the group
    time_ranges = db.session.execute(
        alchemy.select(TimeSlot)
        .where(TimeSlot.groupID == groupID)
    ).scalars().all()

    # Organize time ranges by day
    available_times = {day: [] for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']}
    for time_range in time_ranges:
        available_times[time_range.day].append((time_range.start_time, time_range.end_time))

    if request.method == "GET":
        return render_template("submitResponse.html", title="Apply to Join Group", cssFile="../static/responding_request.css", jsFile="../static/main.js", form=respondingForm, groupID=groupID, group=groupObj, available_times=available_times,userID = loggedInUserID)

    elif request.method == "POST":
        if respondingForm.validate_on_submit():
            foundGroupTime = []
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                for slot in getattr(respondingForm, day).entries:
                    start_time = TimeDay.fromisoformat(slot.start_time.data)
                    end_time = TimeDay.fromisoformat(slot.end_time.data)

                    if not start_time == end_time:
                        if start_time > end_time:
                            flash(f'End time must be after start time for {day.capitalize()}.', 'danger')
                            return render_template('submitResponse.html', title="Apply to Join Group", cssFile="../static/responding_request.css", jsFile="../static/main.js", form=respondingForm, groupID=groupID, group=groupObj, available_times=available_times,userID = loggedInUserID)

                        # Validate if the times are within the group's available times
                        valid_time = False
                        for available_start, available_end in available_times[day]:
                            if start_time >= available_start and end_time <= available_end:
                                valid_time = True
                                break
                        if not valid_time:
                            flash(f'Time slot {start_time} - {end_time} is not within the available times for {day.capitalize()}.', 'danger')
                            return render_template('submitResponse.html', title="Apply to Join Group", cssFile="../static/responding_request.css", jsFile="../static/main.js", form=respondingForm, groupID=groupID, group=groupObj, available_times=available_times,userID = loggedInUserID)

                        new_slot = TimeSlot(
                            userID=loggedInUserID,
                            groupID=groupID,
                            day=day,
                            start_time=start_time,
                            end_time=end_time
                        )
                        db.session.add(new_slot)
                db.session.commit()

                time_ranges = db.session.execute(alchemy.select(TimeSlot).where(TimeSlot.groupID == groupID)).scalars().all()
                people = []
                for time_range in time_ranges:
                    if time_range.day == day:
                        print(time_range)
                        people.append([time_range.userID,str(time_range.start_time),str(time_range.end_time)])
                        print(people)
                        print(groupObj.requiredStudents)
                        print(groupObj.numberOfHours)
                tmp = CheckOverlap(people,groupObj.requiredStudents,groupObj.numberOfHours)
                if tmp != []:
                    tmp[0] = day + "," + tmp[0]
                    foundGroupTime.append(tmp)
            print("hola")
            if foundGroupTime != []:
                print("HELLOOOO")
                others = foundGroupTime[0]
                time = others[0]
                peple = ','.join(str(x) for x in others[1])
                newReply = ReplyMessages(
                    userID=loggedInUserID,
                    groupID=groupID,
                    otherUsers=peple,
                    timeStart=time
                )
                db.session.add(newReply)
            db.session.commit()
            flash('Response submitted successfully!', 'success')
            return redirect(url_for("index"))

    return render_template("submitResponse.html", title="Apply to Join Group", cssFile="../static/responding_request.css", jsFile="../static/main.js", form=respondingForm, groupID=groupID, group=groupObj, available_times=available_times,userID = loggedInUserID)


@app.route('/user_creation', methods=['GET', 'POST'])
def user_creation():
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
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
    return render_template("user_creation.html",title="Register Account - Study Group Organiser",form=regform,cssFile="../static/user_creation.css",jsFile="../static/main.js",userID = loggedInUserID)

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    form = userLogin()
    if form.validate_on_submit() == True:
        user = db.session.scalar(alchemy.select(Users).where(Users.userName == form.studentUser.data))
        if user == None or not user.getPassword(form.studentPwd.data):
            flash("Invalid login details")
        login_user(user)
        return redirect(url_for('index'))
    return render_template("user_login.html",title="Log In - Study Group Organiser",form=form,cssFile="../static/login.css",jsFile="../static/main.js",userID = loggedInUserID)

@app.route('/about')
def about():
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    return render_template("about.html",title="About Us",userID = loggedInUserID)
  
  
@app.route('/logout')
def userLogout():
    logout_user()

    return(redirect(url_for('index')))

@app.route('/user/<int:userID>')
@login_required
def user_page(userID):
    loggedInUserID = 0
    if current_user.is_authenticated:
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    else:
        return redirect(url_for('user_login'))
    username = current_user.userName
    #groups = db.session.scalar(alchemy.select(Groups)
    groups = Groups.query.all()

    notifications = [{"Title":"CITS:2200 exam", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"Book club", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"team all the marks", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     {"Title":"Example Title4", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                     ]
    # groups = []
    # notifications = []


    return render_template("user_page.html",title=username, user=username, groups=groups, cssFile="../static/userpage.css" ,notifications=notifications,userID = loggedInUserID)



@login.user_loader
def getID(userID):
    return db.session.get(Users, int(userID))

@app.errorhandler(401)
def unauthorisedError(error):
    flash("You are not signed in!")
    return redirect(url_for("user_login"))

