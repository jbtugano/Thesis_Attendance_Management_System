from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, DateField, validators, RadioField
from wtforms.validators import DataRequired, URL, Email, Regexp, Length
from sqlalchemy import select
from models import Sections
from db import Session
import datetime

session = Session()


def validate_selection(form, field):
    if field.data == 'Enrolled Section':
        raise validators.ValidationError('Please select a section.')


class LoginForm(FlaskForm):
    user = StringField("Student ID Number/Email Address", validators=[DataRequired()])
    passwd = PasswordField("Password", validators=[DataRequired()])
    checkbox = BooleanField('Checkbox')
    login = SubmitField("Login")


class UserDetails(FlaskForm): #read only
    user = StringField("Name:", render_kw={'readonly': True})
    email = StringField("Email:", validators=[Email()], render_kw={'readonly': True})
    id_num = StringField("Student ID Number:", render_kw={'readonly': True})
    change_email = SubmitField("Change email", name='change_email')
    change_passwd = SubmitField("Change password", name='change_passwd')


class FacultyDetails(FlaskForm):

    fname = StringField("First Name")
    lname = StringField("Last Name")
    email = StringField('')
    id_num = StringField('Employee Number')
    pass
class TestSelect(FlaskForm):

    name = StringField("Name")
    submit = SubmitField("OK")
    section_choices = SelectField('Programming Language')


class DateSelect(FlaskForm):

    datePicker = DateField("Select Date", default=datetime.datetime.today())
    submit = SubmitField("OK")


class DailyReport(FlaskForm):

    section_choices = SelectField('', choices=['Section'], default='Section')
    activity_choices = SelectField('', choices=['Activities'], default='Activities')
    filter = SubmitField("Filter Reports")
    sort_by = SelectField('', choices=['Date', 'Name', 'Course/Program', 'Activity Joined'], default='Date')
    pages = SelectField('', choices=[])
    q = StringField("")


class AttendanceHistory(FlaskForm):

    section_choices = SelectField('', choices=['Section'], default='Section')
    term_choices = SelectField('', choices=['Term', 'Prelim', 'Midterm', 'Finals'], default='Term')
    sort_by = SelectField('', choices=['Name', 'Course/Program'], default='Name')
    q = StringField("")
    submit = SubmitField("Filter Records")
    download = SubmitField("Download Records")


class AdminRegisterStudent(FlaskForm):

    first_name = StringField("", validators=[DataRequired(), Regexp(r'^[A-Za-z ]+$', message="First Name Field must contain only alphabetic letters")])
    middle_name = StringField("", validators=[DataRequired(), Regexp(r'^[A-Za-z.]+$', message="Middle Name Field must contain only alphabetic letters")])
    last_name = StringField("", validators=[DataRequired(), Regexp(r'^[A-Za-z ]+$', message="Last Name Field must contain only alphabetic letters")] )
    student_number = StringField("", validators=[DataRequired()])
    year = SelectField('', choices=['Year', '1st', '2nd', '3rd', '4th', '5th'], default='Year')
    email = StringField("", validators=[DataRequired(), Email()])
    password = StringField("", validators=[DataRequired(), Length(min=13, message="Password must be at least 13 characters long.")])
    course = SelectField('', choices=['Course/Program', 'BS CpE', 'BS IT', 'BS ME', 'BS ECE', 'BS EE'], default='Course/Program')
    section = SelectField('', choices=['Enrolled Section', 'IT 201', 'CS 201', 'ARCH 201', 'ME 201'], validators=[validate_selection])
    submit = SubmitField('Add Student')


class AdminDailyReport(FlaskForm):

    section = SelectField('', choices=['Section'], default='Section')
    activity = SelectField('', choices=['Activity'], default='Activity')
    filter_reports = SubmitField('Filter Reports')
    sort_by = SelectField('', choices=['Sort_by', 'Name', 'Course', 'Activity'], default='Sort_by')
    faculties = SelectField('', choices=['Faculty Name'], default='Faculty Name')
    q = StringField('')


class AdminAttendanceHistory(FlaskForm):

    section = SelectField('', choices=['Section'], default='Section')
    term = SelectField('', choices=['Term', 'Prelim', 'Midterm', 'Finals'], default='Term')
    faculties = SelectField('', choices=['Faculty Name'], default='Faculty Name')
    q = StringField('')
    filter_rows = SubmitField('Filter')
    export_button = SubmitField('Export')
    sort_by = SelectField('', choices=['Sort_by', 'Name', 'Course', 'Progress'], default='Sort_by')
    archive_button = SubmitField('Archive')


class AdminManageFaculty(FlaskForm):

    sort_by = SelectField('', choices=['Name'])
    q = StringField('')


class AdminManageFacultyDetails(FlaskForm):

    sort_by = SelectField('', choices=['Section', 'Day', 'Time Period'], default='Day')
    q = StringField('')


class AdminManageStudent(FlaskForm):

    sort_by = SelectField('', choices=['Select', 'Name', 'Course', 'Section'], default='Select')
    faculties = SelectField('', choices=['Faculty Name'], default='Faculty Name')
    q = StringField('')


class AdminAddFaculty(FlaskForm):

    fn = StringField('', validators=[DataRequired()])
    mn = StringField('', validators=[DataRequired()])
    ln = StringField('', validators=[DataRequired()])
    employee_id = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired(), Email()])
    password = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add')


class AdminEditFaculty(FlaskForm):

    fn = StringField('', validators=[DataRequired()])
    mn = StringField('', validators=[DataRequired()])
    ln = StringField('', validators=[DataRequired()])
    employee_id = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired(), Email()])
    password = StringField('', validators=[DataRequired()])
    submit = SubmitField('Edit')


class AdminAddActivity(FlaskForm):

    aname = StringField('', validators=[DataRequired()])
    adesc = StringField('', default="Lorem ipsum dolor sit")
    alim = StringField('', default="40")
    aadd = SubmitField('Add')


class AdminEditActivity(FlaskForm):

    aid = StringField('')
    aname = StringField('', validators=[DataRequired()])
    adesc = StringField('', default="Lorem ipsum dolor sit")
    alim = StringField('', default="40")
    aoff = RadioField('', choices=['Yes', 'No'], default="Yes")
    save = SubmitField('Save Changes')


class AdminAddClasses(FlaskForm):

    time_choices = [
        (1, '7:00AM'),
        (2, '7:30AM'),
        (3, '8:00AM'),
        (4, '8:30AM'),
        (5, '9:00AM'),
        (6, '9:30AM'),
        (7, '10:00AM'),
        (8, '10:30AM'),
        (9, '11:00AM'),
        (10, '11:30AM'),
        (11, '12:00PM'),
        (12, '12:30PM'),
        (13, '01:00PM'),
        (14, '01:30PM'),
        (15, '02:00PM'),
        (16, '02:30PM'),
        (17, '03:00PM'),
        (18, '03:30PM'),
        (19, '04:00PM'),
        (20, '04:30PM'),
        (21, '05:00PM')
    ]

    sec_name = StringField('', validators=[DataRequired()])
    fac_name = SelectField('', choices=[])
    day_select = SelectField('', choices=[('M', 'MONDAY'), ('T', 'TUESDAY' ), ('W', 'WEDNESDAY'), ('TH', 'THURSDAY'), ('F', 'FRIDAY'), ('S', 'SATURDAY')], default='M')
    act_select = SelectField('', choices=[])
    time_select = SelectField('', choices=time_choices, default=1)
    add_button = SubmitField('Add Class')

class AdminManageActivity(FlaskForm):

    q = StringField('')


class AdminEditStudent(FlaskForm):

    first_name = StringField("", validators=[Regexp(r'^[A-Za-z ]+$', message="First Name Field must contain only alphabetic letters")])
    middle_name = StringField("", validators=[Regexp(r'^[A-Za-z.]+$', message="Middle Name Field must contain only alphabetic letters")])
    last_name = StringField("", validators=[Regexp(r'^[A-Za-z ]+$', message="Last Name Field must contain only alphabetic letters")])
    student_number = StringField("")
    email = StringField("", validators=[Email()])
    password = StringField("", validators=[Length(min=13, message="Password must be at least 13 characters long.")])
    course = SelectField('', choices=['Course/Program', 'BS CpE', 'BS IT', 'BS ME', 'BS ECE', 'BS EE'])
    section = SelectField('', choices=['Enrolled Section', 'IT 201', 'CS 201', 'ARCH 201', 'ME 201'], validators=[validate_selection])
    edit = SubmitField('Save Details')
