from flask_wtf import FlaskForm as form
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, IntegerField, DateField, BooleanField, FieldList, FormField, HiddenField, TimeField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
import sqlalchemy as alchemy
from app import db
from app.models import Users, Groups, TimeSlot
from datetime import time

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

# def validate_time_range(form, field):
#     start_time = field.data
#     stop_time = form[field.name.replace('start', 'stop')].data

#     if start_time >= stop_time:
#         raise ValidationError('Start time must be before stop time.')

# def create_day_forms():
#     day_forms = {}
#     days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     for day in days_of_week:
#         start_time_field = TimeField(f'Start Time ({day}) (HH:MM)', validators=[InputRequired(), validate_time_range])
#         stop_time_field = TimeField(f'Stop Time ({day}) (HH:MM)', validators=[InputRequired(), validate_time_range])

#         setattr(TimeRangeForm, f'{day.lower()}StartTime', start_time_field)
#         setattr(TimeRangeForm, f'{day.lower()}StopTime', stop_time_field)

#     return TimeRangeForm()

# /////////////////////////////////////////////////////////////////////////////
def validate_csrf_token(self, field):
        if not self.csrf_enabled:
            return True
        if hasattr(request, 'csrf_valid') and request.csrf_valid:
            # this is validated by CsrfProtect
            return True
        if not validate_csrf(field.data, self.SECRET_KEY, self.TIME_LIMIT):
            raise ValidationError(field.gettext('CSRF token missing'))

def validate_time_slot(form, field):
    day_slots = TimeSlot.query.filter_by(day=form.day.data).all()
    for slot in day_slots:
        if not (field.start_time.data >= slot.end_time or field.end_time.data <= slot.start_time):
            raise ValidationError("Time slot overlaps with an existing slot.")

def time_choices():
    times = [(time(hour, minute).strftime("%H:%M"), time(hour, minute).strftime("%H:%M"))
             for hour in range(0, 24)
             for minute in range(0, 60, 15)]
    return times

class TimeSlotForm(form):
    day = HiddenField()
    start_time = SelectField('Start Time', choices=time_choices(), validators=[DataRequired()])
    end_time = SelectField('End Time', choices=time_choices(), validators=[DataRequired(), validate_time_slot])

class TimeSlotFormNoCsrf(form):
    day = HiddenField()
    start_time = SelectField('Start Time', choices=time_choices(), validators=[DataRequired()])
    end_time = SelectField('End Time', choices=time_choices(), validators=[DataRequired(), validate_time_slot])
    def __init__(self, *args, **kwargs):
        super(TimeSlotFormNoCsrf, self).__init__(meta={'csrf':False}, *args, **kwargs)

class WeekForm(form):
    print("here 1.1")
    groupTitle = StringField("Group Title: ")
    groupTag1 = StringField("Group Tag: ")
    groupTag2 = StringField("Second Group Tag: ")
    groupTag3 = StringField("Third Group Tag: ")
    description = StringField("Description / Reason For Study Group: ")
    groupRequestSubmition = SubmitField("Submit Group Request")
    
    monday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3) #needs to pared with other fields to be safe 
    tuesday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    wednesday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    thursday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    friday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    saturday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    sunday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)

    submit = SubmitField('Save')
# /////////////////////////////////////////////////////////////////////////////

class submitTimes(form):
    submit = SubmitField('Submit')
    def validateStudentUsername(self, groupTitle):
        userName = db.session.scalar(alchemy.select(Groups).where(Groups.username == groupTitle.data))
        if userName is not None:
            raise ValidationError("Group name is already taken, please try another.")

class replyForm(form):
    message = StringField("Enter group message: ")
    monday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3) #needs to pared with other fields to be safe 
    tuesday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    wednesday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    thursday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    friday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    saturday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    sunday = FieldList(FormField(TimeSlotFormNoCsrf), min_entries=1, max_entries=3)
    submit = SubmitField("Submit Response")
