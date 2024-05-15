from flask_wtf import FlaskForm as form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
import sqlalchemy as alchemy
from app import db
from app.models import Users, Groups, ReplyMessages

class userRegister(form):
    studentFN = StringField("Full Name: ", validators=[DataRequired()])
    studentUN = StringField("User Name: ")
    studentEM = StringField("Email Address: ", validators=[DataRequired(), Email()])
    studentPW = PasswordField("Password: ", validators=[DataRequired()])
    studentCW = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo('studentPW')])
    submitButton = SubmitField("Create Account")
    def validateStudentUsername(self, studentUN):
        userName = db.session.scalar(alchemy.select(Users).where(Users.username == studentUN.data))
        if userName is not None:
            raise ValidationError("Username is already taken, please try another.")
    def emailDuplicateValidation(self, studentEM):
        emailAddr = db.session.scalar(alchemy.select(Users).where(Users.studentEM == studentEM.data))
        if emailAddr is not None:
            raise ValidationError("Email address already in use. Please try with a different email address.")
class userLogin(form):
    studentUser = StringField("Username: ", validators=[DataRequired()])
    studentPwd = PasswordField("Password: ", validators=[DataRequired()])
    loginButton = SubmitField("Log In")

class submitTimes(form):
    groupTitle = StringField("Group Title: ", validators=[DataRequired()])
    groupTag1 = StringField("Group Tag: ")
    groupTag2 = StringField("Second Group Tag: ")
    groupTag3 = StringField("Third Group Tag: ")
    Description = StringField("Description / Reason For Study Group: ")
    groupRequestSubmition = SubmitField("Submit Group Request")
    mondayStartTime = TimeField('start on monday')
    mondayEndTime = TimeField('end of available time')
    tuesdayStartTime = TimeField('start on tuesday')
    tuesdayEndTime = TimeField('end of available time')
    webnesdayStartTime = TimeField('start on webnesday')
    webnesdayEndTime = TimeField('end of available time')
    thursdayStartTime = TimeField('start on thursday')
    thursdayEndTime = TimeField('end of available time')
    fridayStartTime = TimeField('start on friday')
    fridayEndTime = TimeField('end of available time')
    saterdayStartTime = TimeField('start on saterday')
    saterdayEndTime = TimeField('end of available time')
    sundayStartTime = TimeField('start on sunday')
    sundayEndTime = TimeField('end of available time')
    def validateStudentUsername(self, groupTitle):
        userName = db.session.scalar(alchemy.select(Groups).where(Groups.username == groupTitle.data))
        if userName is not None:
            raise ValidationError("Group name is already taken, please try another.")
