from flask_wtf import FlaskForm as form
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
import sqlalchemy as alchemy
from app import db
from app.models import Users, Groups

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

class initialiseGroup(form):
    groupTitle = StringField("Group Title: ", validators=[DataRequired()])
    tagOne = StringField("Select first tag: ", validators=[DataRequired()]) #set this as a Bootstrap dropdown
    tagTwo = StringField("Select second tag: ")
    tagThree = StringField("Select third tag: ")
    groupDesc = StringField("Group Description: ")
    availStart = DateField("Select Availablility Start: ", validators=[DataRequired()])
    availEnd = DateField("Select Availability End: ", validators=[DataRequired()])
    requiredStudents = IntegerField("Required number of students: ", validators=[DataRequired()])
    submitButton = SubmitField("Create New Group")

class replyGroup:
    availStart = DateField("Select start of available time: ", validators=[DataRequired()]) # VERIFY!
    availEnd = DateField("Select end of availability time: ", validators=[DataRequired()]) # VERIFY!!