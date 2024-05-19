from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login
import sqlalchemy as alchemy
from sqlalchemy.sql import text

from app.models import Users, Groups, TimeSlot
from app.forms import userLogin, userRegister, submitTimes, TimeSlotForm, WeekForm, replyForm
from datetime import time
import json
from ast import literal_eval # NOT THE BEST IDEA, BUT IT WORKS ANYWAY

@app.route('/')
@app.route('/index')
def index():
    availableGroups = Groups.query.all()
    user = Users.query.all()
    units = db.session.query(Groups.tagOne).order_by(alchemy.desc(Groups.tagOne)).all()
    return render_template("index.html",title="Study Group Organiser Application",user=user,groups=availableGroups,cssFile="../static/index.css",jsFile="../static/main.js", units=units)

@app.route('/createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    form = WeekForm()
    if form.validate_on_submit():
        # Create and save the Group instance
        loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
        print("User ID: {}".format(loggedInUserID))
        # Save the TimeSlot instances
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            for slot in getattr(form, day).entries:
                start_time = time.fromisoformat(slot.start_time.data)
                end_time = time.fromisoformat(slot.end_time.data)
                if not start_time == end_time:
                    if start_time > end_time:
                        flash(f'End time must be after start time for {day.capitalize()}.', 'danger')
                        return render_template('createGroup.html', form=form)
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
            members=groupStr
        )
        db.session.add(group)
        db.session.commit()
        currentMembership = db.session.scalar(alchemy.select(Users.groupMembership).where(loggedInUserID == Users.userID))
        groupID = db.session.scalar(alchemy.select(Groups.groupID).where(Groups.groupTitle == form.groupTitle.data))
        if currentMembership is None:
            newMembership = []
            newMembership.append(str(groupID))
        else:
            print("Membership: ", currentMembership)
            newMembership = currentMembership.split("---")
            print("New membership: {}".format(newMembership))
            newMembership.append(str(groupID))
        memberString = "---".join(newMembership)
        print("Membership: {}".format(memberString))
        db.session.query(Users).filter(Users.userID == loggedInUserID).update({"groupMembership": memberString})
        db.session.commit()
        print("New Membership: {}".format(db.session.scalar(alchemy.select(Users.groupMembership).where(loggedInUserID == Users.userID))))

        # Save the TimeSlot instances
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            for slot in getattr(form, day).entries:
                start_time = time.fromisoformat(slot.start_time.data)
                end_time = time.fromisoformat(slot.end_time.data)
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


@app.route('/submitResponse/<int:groupID>', methods=["GET", "POST"])
@login_required
def submitResponse(groupID):
    print("Do you hear me?")
    loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    groupObj = db.session.scalar(alchemy.select(Groups).where(Groups.groupID == groupID))
    respondingForm = replyForm()
    timeslots = db.session.scalar(alchemy.select(TimeSlot).where(groupID == TimeSlot.groupID).where(Groups.userID == TimeSlot.userID))
    specifiedGroupObject = db.session.scalar(alchemy.select(Groups).where(groupID == Groups.groupID))

    days = db.session.scalars(alchemy.select(TimeSlot.day)
            .join(Groups, (Groups.groupID == TimeSlot.groupID) & (Groups.userID == TimeSlot.userID))
            .distinct()
        ).all()
    groupDesc = db.session.scalar(alchemy.select(Groups.description).where(Groups.groupID == groupID))
    loggedInUserID = db.session.scalar(alchemy.select(Users.userID).where(current_user.userName == Users.userName))
    if request.method == "GET":
        return render_template("submitResponse.html",title="Apply to Join Group",cssFile="../static/responding_request.css",jsFile="../static/main.js", form=respondingForm, groupID=groupID, group=groupObj, timeslots=days, groupDesc=groupDesc)
    elif request.method == "POST":
        if respondingForm.validate_on_submit():
            for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                for slot in getattr(respondingForm, day).entries:
                    start_time = time.fromisoformat(slot.start_time.data)
                    end_time = time.fromisoformat(slot.end_time.data)
                    if not start_time == end_time:
                        if start_time > end_time:
                            flash(f'End time must be after start time for {day.capitalize()}.', 'danger')
                            return render_template('createGroup.html', form=respondingForm)
                        new_slot = TimeSlot(
                            userID=loggedInUserID,
                            groupID=groupID,
                            day=day,
                            start_time=start_time,
                            end_time=end_time
                        )
                        db.session.add(new_slot)
                db.session.commit()
            
            currentMembership = db.session.scalar(alchemy.select(Users).where(loggedInUserID == Users.userID))
            if currentMembership is None:
                newMembership = [str(groupID)]
            else:
                newMembership = currentMembership.split("---")
                newMembership.append(str(groupID))
            memberString = "---".join(newMembership)
            mlString = db.session.scalar(alchemy.select(Groups).where(groupID == Groups.groupID))
            mlList = mlString.split("---")
            mlList.append(str(loggedInUserID))
            newString = "---".join(mlList)
            db.session.query(Users).filter(Users.userID == loggedInUserID).update({"groupMembership": memberString})
            db.session.query(Groups).filter(Groups.groupID == groupID).update({"members": newString})
            db.session.commit()
        return redirect(url_for("index"))
    #return render_template("submitResponse.html",title="Apply to Join Group",cssFile="../static/responding_request.css",jsFile="../static/main.js", form=respondingForm, groupID=groupID)

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
    loggedInUser = db.session.scalar(alchemy.select(Users.userID).where(Users.userName == current_user.userName))
    userGroups = str(db.session.scalar(alchemy.select(Users.groupMembership).where(loggedInUser == Users.userID)))
    print("Userpage Groups: {}".format(userGroups))
    availableGroups = {}
    groupNames = []
    index = 0
    print(userGroups == "None")
    if userGroups == "None":
        groupNames = "User is not a member of any groups!"
        print(groupNames)

    else:
        print("Usergroups: {}".format(userGroups))
        groupMembership = userGroups.split("---")
        for item in groupMembership:
            emailList = []
            groupTitle = db.session.scalar(alchemy.select(Groups.groupTitle).where(item == Groups.groupID))
            userIDs = str(db.session.scalar(alchemy.select(Groups.members).where(item == Groups.groupID)))
            idList = userIDs.split("---")
            for item in idList:
                studentEmail = db.session.scalar(alchemy.select(Users.userEmail).where(item == Users.userID))
                emailList.append(studentEmail)
            availableGroups[groupTitle] = {"ID": item, "timedate":"placeholder", "emails":emailList}
            groupNames.append(groupTitle)
    print("Groupnames: {}".format(groupNames))

    print("Available Groups: {}".format(availableGroups))

    #notifications = [{"Title":"CITS:2200 exam", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                    #  {"Title":"Book club", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                    #  {"Title":"team all the marks", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                    #  {"Title":"Example Title4", "timedate":["31st at 0100-0800","19th at 1100-2100"],"emails":["23631345@student.uwa.edu.au","12345678@email.com.au"]},
                    # ]
    # groups = []
    # notifications = []


    return render_template("user_page.html",title=username, user=username, groups=groupNames, cssFile="../static/userpage.css" ,notifications=availableGroups)



@login.user_loader
def getID(userID):
    return db.session.get(Users, int(userID))

@app.errorhandler(401)
def unauthorisedError(error):
    flash("You are not signed in!")
    return redirect(url_for("user_login"))
