from flask_wtf import FlaskForm as ff
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
import sqlalchemy as alchemy
from app import db
from app.models import Users

class userRegister(ff):
    studentFN = StringField("Full Name: ", validators=[DataRequired()])
    studentUN = StringField("User Name: ")
    studentEM = StringField("Email Address: ", validators=[DataRequired(), Email()])
    studentPW = PasswordField("Password: ", validators=[DataRequired()])
    studentCW = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo(studentPW)])
    submitButton = SubmitField("Create Account")
    def validateStudentUsername(self, studentUN):
        userName = db.session.scalar(alchemy.select(Users).where(Users.username == studentUN.data))
        if userName is not None:
            raise ValidationError("Username is already taken, please try another.")
    def emailDuplicateValidation(self, studentEM):
        emailAddr = db.session.scalar(alchemy.select(Users).where(Users.studentEM == studentEM.data))
        if emailAddr is not None:
            raise ValidationError("Email address already in use. Please try with a different email address.")
class userLogin(ff):
    studentUser = StringField("Username: ", validators=[DataRequired()])
    studentPwd = PasswordField("Password: ", validators=[DataRequired()])
    loginButton = SubmitField("Log In")