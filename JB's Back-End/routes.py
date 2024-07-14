from flask import Flask, redirect, render_template, url_for, request, abort
from forms import UserDetails, LoginForm, TestSelect
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from sqlalchemy import create_engine, select, or_, and_
from sqlalchemy.orm import sessionmaker
from models import UserRoles, LoginInfo, Students, Faculty, DaySummary, ClassInfo
from db import Session
from werkzeug.security import generate_password_hash, check_password_hash


# create instance
session = Session()

# connect flask
app = Flask(__name__, template_folder='templates') #readjust template folder
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# configure login manager, connect to flask app
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.execute(select(LoginInfo).where(LoginInfo.id == user_id)).scalar()


# require login
def login_required(f):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["POST", "GET"], endpoint='home')
@login_required
def home():

    if current_user.user_role.user_level == 2: # role level 2 == student
        form = UserDetails()
        user_info = session.execute(select(Students).where(Students.id_number == current_user.user_id)).scalar()
        return render_template("Student Website/student-dashboard.html", form=form, user_info=user_info)
    else:
        user_info = session.execute(select(Faculty).where(Faculty.id_number == current_user.user_id)).scalar()

        return render_template("Faculty Website/faculty-dashboard.html", user_info=user_info)

#    if request.method == "POST":
#        action = list(request.form)[3]
#        if action == "change_email":
#            print("Changing email")
#        elif action == "change_passwd":
#            print("Changing password")
#        else:
#            print("Not allowed")
#        return render_template("formtest.html", form=form)
    #return render_template("Student Website/student-dashboard.html", form=form, user_info=user_info)


@app.route("/login", methods=["POST", "GET"], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST": #login attempt

        username = form.user.data
        password = form.passwd.data
        existing_user = session.execute(select(LoginInfo).filter(or_(LoginInfo.email == username, LoginInfo.user_id == username))).scalar()
        if existing_user:

            if not check_password_hash(existing_user.passwd, password):
                return redirect(url_for("login"))

            if form.checkbox.data:
                login_user(existing_user, remember=True)
            else:
                login_user(existing_user)

            return redirect(url_for("home"))

        return redirect(url_for("login"))

    return render_template("Student Website/homepage.html", form=form)


@app.route("/user_profile", endpoint='profile')
@login_required
def profile():
    student_info = session.execute(select(Students).where(Students.id_number == current_user.user_id)).scalar()
    form = UserDetails()
    form.id_num.data = current_user.user_id
    form.email.data = current_user.email
    form.user.data = current_user.user_role.students.name
    #clicking change email/passwd button will redirect to specified route
    #if not is_new, click on button will send a link to user email
    #store token to db
    #link will direct to specific path, parameter is the token generated
    return render_template("Student Website/student-settings-accountinfo.html", form=form, info=student_info)


@app.route("/change_password/<token>", methods=["GET"], endpoint='change_password')
def change_password(token):
    # TODO #100 ADD THIS FEATURE
    if request.method == "POST":
        return f"<h1> {token} </h1>"


@app.route("/change_email/<token>", methods=["GET"])
def change_email(token):
    # TODO #101 ADD THIS FEATURE
    return f"<h1>hello {token} </h1>"


@app.route("/logout", endpoint="logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/view_attendance", endpoint="view_attendance")
@login_required
def view_attendance():
    student_records = session.execute(select(DaySummary).where(DaySummary.student_id == current_user.user_role.students.id)).scalars().all()
    return render_template("Student Website/student-attendance-records.html", records=student_records)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html', error=e), 403, {"Refresh": f"1; url={url_for('login')}"}


@app.route("/debug")
def debug():
    return "<h1>debug</h1>"


# FACULTY ROUTES

@app.route('/daily_report')
def daily_report():
    # Attendance Today
    own_classes = session.execute(select(ClassInfo).where(ClassInfo.facultyid == current_user.user_role.faculties.id)).scalars().all()

    aaa = session.execute(select(DaySummary)).scalars().all()

    asda = [i for i in aaa if i.class_info in own_classes]
    print(asda)
    '''
    for i in aaa:
        print("hey", end="")
        if i.class_id in classes:
            print("yuh")
    '''
    return render_template('Faculty Website/faculty-classes-attendance-records.html', own_classes=own_classes, students=asda)


@app.route('/enrolled_students')
def enrolled_students():
    # Enrolled Students
    user_info = session.execute(select(Faculty).where(Faculty.id_number == current_user.user_id)).scalar()

    #for aclass in user_info.classes:
    #    print(aclass.section.name)

    return render_template('Faculty Website/faculty-classes-enrolledstudents.html', user_info=user_info)


@app.route('/attendance_history')
def attendance_history():
    # Attendance History

    return render_template('Faculty Website/faculty-attendance-history.html')


@app.route('/faculty_info')
def faculty_info():
    # Account Information
    return render_template('Faculty Website/faculty-settings-accountinfo.html')


@app.route('/faculty_pw')
def faculty_pw():
    # Account Password
    return render_template('Faculty Website/faculty-settings-password.html')


@app.route('/test', methods=['POST', 'GET'])
def selectTest():
    form = TestSelect()
    if request.method == "POST":
        print(form.choices.data)
    return render_template('test/selectTest.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    