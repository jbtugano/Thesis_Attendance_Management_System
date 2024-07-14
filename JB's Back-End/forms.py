from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, Email
#from flask_ckeditor import CKEditorField


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


class TestSelect(FlaskForm):
    name = StringField("Name")
    submit = SubmitField("OK")
    choices = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])