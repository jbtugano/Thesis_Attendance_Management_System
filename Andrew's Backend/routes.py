import time
import pandas as pd
from flask import Flask, flash, redirect, render_template, url_for, request, abort, send_from_directory, session as s
from forms import (UserDetails, LoginForm, TestSelect, DateSelect, DailyReport, AdminRegisterStudent, AttendanceHistory,
                   AdminDailyReport, AdminAttendanceHistory, AdminManageFaculty, AdminManageFacultyDetails,
                   AdminAddFaculty, AdminEditFaculty, AdminEditActivity, AdminAddActivity, FacultyDetails,
                   AdminAddClasses, AdminEditStudent, AdminManageStudent, AdminManageActivity)
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_fresh
from sqlalchemy import create_engine, select, or_, and_, func, text
from models import (UserRoles, LoginInfo, Students, Faculty, DaySummary, ClassInfo, Sections,
                    Term, Semester, AcademicYear, Activities, Schedule)
from db import Session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from deepface import DeepFace
from itsdangerous import URLSafeTimedSerializer

# create instance
session = Session()

# connect flask
app = Flask(__name__, template_folder='templates') #readjust template folder
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
flask_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
EXCEL_DIRECTORY = 'excel_files'
os.makedirs(EXCEL_DIRECTORY, exist_ok=True)
os.makedirs('static/ACTIMAGES', exist_ok=True)
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


def prof_required(f):

    def wrapper2(*args, **kwargs):
        if current_user.user_role.user_level != 1:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper2


def student_required(f):

    def wrapper3(*args, **kwargs):
        if current_user.user_role.user_level != 2:
            return abort(403)
        return f(*args, **kwargs)
    return wrapper3

"""DeepFace.find(
    img_path='static/uploads/ATTEMPTS/34.jpg',
    db_path='static/uploads/ref',
    model_name='Facenet512',
    detector_backend='ssd'
)"""


@app.route('/drew2test')
def drew2test():
    s = 'wacse15@gmail.com'
    token_g = flask_serializer.dumps(s, salt='email-confirm-salt')
    reset_url = url_for('change_details', token=token_g, _external=True)
    print(reset_url)
    return render_template('drew.html')


@app.route('/', endpoint='landing_page')
def landing_page():
    return render_template('homepage/index.html')


@app.route('/contactus', endpoint='contactus_page')
def contactus_page():
    return render_template('homepage/contacts.html')


@app.route('/about', endpoint='aboutus_page')
def aboutus_page():
    return render_template('homepage/about.html')


@app.route('/change_details/<token>', methods=['GET', 'POST'])
def change_details(token):
    try:
        email = flask_serializer.loads(token, salt='email-confirm-salt', max_age=3600)
        print(email)
    except Exception as e:
        print(e)
    print("success")


@app.route("/home", methods=["POST", "GET"], endpoint='home')
@login_required
def home():


    if current_user.user_role.user_level == 2: # role level 2 == student
        if current_user.user_role.students.progress >= 50 and login_fresh(): #modify to threshold value
            if not s.get('notification_viewed'):
                s['notification_viewed'] = True
                return render_template('notifications.html')

        form = UserDetails()
        user_info = session.execute(select(Students).where(Students.id_number == current_user.user_id)).scalar()
        return render_template("Student Website/student-dashboard.html", form=form, user_info=user_info)
    else:
        user_info = session.execute(select(Faculty).where(Faculty.id_number == current_user.user_id)).scalar()
        today_date = datetime.datetime.now().strftime("%m-%d-%y")
        today_record = session.execute(select(DaySummary).filter(func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date)).scalars().all()
        #today_record = session.execute(select(DaySummary)).scalars().all()
        tr_count = [i for i in today_record if i.class_info.faculty.id_number == current_user.user_id]
        tr_count = len(tr_count)

        return render_template("Faculty Website/faculty-dashboard.html", user_info=user_info, trcount=tr_count)

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
    #time.sleep(1200)

    # TODO URGENT : INPUT VALIDATION TO PREVENT SHELL COMMANDS
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
@student_required
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


@app.route("/change_password", endpoint='change_password')
@student_required
def change_password():
    return render_template("Student Website/student-settings-password.html")


@app.route("/change_password/<token>", methods=["GET"])
def change_password_step2(token):
    # TODO #100 ADD THIS FEATURE
    if request.method == "POST":
        return f"<h1> {token} </h1>"


@app.route("/change_email/<token>", methods=["GET"])
def change_email(token):
    # TODO #101 ADD THIS FEATURE
    return f"<h1>hello {token} </h1>"


@app.route("/logout", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/view_attendance", endpoint="view_attendance")
@student_required
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
    date = datetime.datetime.now()
    return render_template("test/date.html", date=date)


# FACULTY ROUTES

@app.route('/daily_report', methods=["GET", "POST"], endpoint='daily_report')
@prof_required
def daily_report():
    # Attendance Today
    # TODO daily_report 1: add facult level only ( user level 1 )

    form = DailyReport()


    own_classes = session.execute(select(ClassInfo).where(ClassInfo.facultyid == current_user.user_role.faculties.id)).scalars().all()
    if request.method == "POST":
        zxcadwqe = form.section_choices.data
        print(zxcadwqe)
        print("THIS IS A POST")
    # fill sections
    own_sections = session.execute(select(Faculty).where(Faculty.id_number == current_user.user_id)).scalar()
    own_sections = [section for section in own_sections.sections]
    handled_sections = [i.name for i in own_sections]
    form.section_choices.choices += handled_sections

    # fill activities
    handled_activities = [i.activity.name for i in own_classes]
    if handled_activities:
        form.activity_choices.choices += handled_activities

    # get all daysummary entries
    aaa = session.execute(select(DaySummary)).scalars().all()
    today_date = datetime.datetime.now().strftime("%m-%d-%y")

    # get only entries from handled classes
    asda = [i for i in aaa if i.class_info in own_classes and i.date_time.strftime("%m-%d-%y") == today_date]
    #asda = [i for i in aaa if i.class_info in own_classes]


    # enable selection
    sec = None if form.section_choices.data == form.section_choices.default else form.section_choices.data
    act = None if form.activity_choices.data == form.activity_choices.default else form.activity_choices.data
    query = "" if form.q.data is None else form.q.data.lower()
    sorted_by = form.sort_by.data

    asda = [ds for ds in asda if (query in ds.student.name.lower()) and
            (sec == ds.class_info.section.name or sec is None) and
            (act == ds.class_info.activity.name or act is None)]

    test_dic = {
        "Date": sorted(asda, key=lambda asda: asda.date_time, reverse=False),
        "Name": sorted(asda, key=lambda asda: asda.student.name.split(","), reverse=False),
        "Course/Program": sorted(asda, key=lambda asda: asda.student.program, reverse=False),
        "Activity Joined": sorted(asda, key=lambda asda: asda.class_info.activity.name, reverse=False)
    }

    asda = test_dic.get(sorted_by, test_dic["Date"])

    #

    return render_template('Faculty Website/faculty-classes-attendance-records.html', own_classes=own_classes, students=asda, form=form)


@app.route('/daily_report/<student>', endpoint='view_daily_student')
@prof_required
def view_daily_student(student):
    student_info = session.execute(select(Students).where(Students.id_number == student)).scalar()
    today_record = session.execute(select(DaySummary).where(DaySummary.student_id == student_info.id)).scalars().all()
    today_date = datetime.datetime.now().strftime("%m-%d-%y")
    today_record = session.execute(select(DaySummary).filter(and_(DaySummary.student_id == student_info.id, func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date))).scalars().all()

    return render_template("Faculty Website/details-faculty-classes-attendance-records.html", student=student_info, records=today_record)


@app.route('/enrolled_students', endpoint='enrolled_students')
@prof_required
def enrolled_students():
    # Enrolled Students

    user_info = session.execute(select(Faculty).where(Faculty.id_number == current_user.user_id)).scalar()



    #for aclass in user_info.classes:
    #    print(aclass.section.name)

    return render_template('Faculty Website/faculty-classes-enrolledstudents.html', user_info=user_info)


@app.route('/attendance_history', methods=['POST', 'GET'], endpoint='attendance_history')
@prof_required
def attendance_history():
    # Attendance History
    form = AttendanceHistory()

    own_classes = session.execute(select(Sections).where(Sections.facultyid == current_user.user_role.faculties.id)).scalars().all()

    # fill sections
    handled_sections = [i.name for i in own_classes]
    form.section_choices.choices += handled_sections

    # fill rows
    handled_students = []
    for s in own_classes:
        for student in s.students:
            handled_students.append(student)


    # enable sorting, query
    sec = None if form.section_choices.data == form.section_choices.default else form.section_choices.data
    term = None if form.term_choices.data == form.term_choices.default else form.term_choices.data
    query = "" if form.q.data is None else form.q.data.lower()
    sorted_by = form.sort_by.data


    asda = [ds for ds in handled_students if (query in ds.name.lower()) and
            (sec == ds.section.name or sec is None)]

    test_dic = {
        "Name": sorted(asda, key=lambda asda: asda.name.split(","), reverse=False),
        "Course/Program": sorted(asda, key=lambda asda: asda.program, reverse=False)
    }

    asda = test_dic.get(sorted_by, test_dic["Name"])


    term_range = session.execute(select(Term).filter(and_(Term.name == term, Term.start <= datetime.datetime.now(), Term.semester.has(Semester.end >= datetime.datetime.now())))).scalar()

    if term_range:
        valid_data = session.execute(select(DaySummary).filter(and_(DaySummary.date_time >= term_range.start, DaySummary.date_time <= term_range.end))).scalars().all()
        inrange_query = [s.student.id_number for s in valid_data]

        valid_dict = {}

        for asd in asda:
            valid_dict[asd.id_number] = inrange_query.count(asd.id_number) * 2 # multiplied by 2 because each entry is 2hours worth

        if 'download' in list(request.form):

            data = [{"STUDENT NAME": student.name,
                     "STUDENT NUMBER": student.id_number,
                     "PROGRAM": student.program,
                     "SECTION": student.section.name,
                     "PROGRESS (hrs)": valid_dict.get(student.id_number, 0)
                     } for student in asda]

            df = pd.DataFrame(data)
            file_name = f"{form.term_choices.data}-{current_user.user_role.faculties.name}-{datetime.datetime.now().strftime('%B%d%Y-%H%M')}"
            df.to_excel(f'{EXCEL_DIRECTORY}/{file_name}.xlsx', index=False)

            # send file to user

            try:
                return send_from_directory(EXCEL_DIRECTORY, f"{file_name}.xlsx", as_attachment=True)
            except:
                return "File does not exist :(", 404

        return render_template('Faculty Website/faculty-attendance-history.html', sections=handled_sections, students=asda, form=form, vd=valid_dict)

    # prep for download
    if 'download' in list(request.form):
        data = [{"STUDENT NAME": student.name,
                 "STUDENT NUMBER": student.id_number,
                 "PROGRAM": student.program,
                 "SECTION": student.section.name,
                 "PROGRESS (hrs)": student.progress
                 } for student in asda]

        df = pd.DataFrame(data)
        file_name = f"FULL SEMESTER-{current_user.user_role.faculties.name}-{datetime.datetime.now().strftime('%B%d%Y-%H%M')}"
        df.to_excel(f'{EXCEL_DIRECTORY}/{file_name}.xlsx', index=False)

    # send file to user

        try:
            return send_from_directory(EXCEL_DIRECTORY, f"{file_name}.xlsx", as_attachment=True)
        except:
            return "File does not exist :(", 404


    return render_template('Faculty Website/faculty-attendance-history.html', sections=handled_sections, students=asda, form=form)



@app.route('/attendance_history/<student>', endpoint='attendance_history_details')
@prof_required
def attendance_history_details(student):

    student_info = session.execute(select(Students).where(Students.id_number == student)).scalar()

    records = session.execute(select(DaySummary).where(DaySummary.student_id == student_info.id)).scalars().all()
    print(student_info.name, records)

    return render_template('Faculty Website/details-faculty-attendance-history.html', student=student_info, records=records)


@app.route('/faculty_info', endpoint='faculty_info')
@prof_required
def faculty_info():
    # Account Information
    form = FacultyDetails()
    name = current_user.user_role.faculties.name
    name_split = name.split(",")
    sec_half = name_split[1].strip().split(" ")
    ln = name_split[0]
    mn = sec_half[-1]
    fn = " ".join(sec_half[0:-1])
    names = [fn, mn, ln]
    return render_template('Faculty Website/faculty-settings-accountinfo.html', form=form, name=names)


@app.route('/faculty_pw', endpoint='faculty_pw')
@prof_required
def faculty_pw():
    # Account Password
    return render_template('Faculty Website/faculty-settings-password.html')


@app.route('/test', methods=['POST', 'GET'])
def selectTest():
    form = TestSelect()
    # try accessing on student, getting handled_sections will result to NoneType so try catch is recommended
    handled_sections = session.execute(select(Sections).where(Sections.facultyid == current_user.user_role.faculties.id)).scalars().all()
    if handled_sections:
        sections = [section.name for section in handled_sections]
        form.section_choices.choices = sections
    print(request.method)
    if request.method == "POST":
        if form.section_choices.data not in sections:
            print("CHEATER")
        else:
            # return a render template
            print(form.section_choices.data)
            return redirect(url_for('selectTest', section=form.section_choices.data))
    return render_template('test/selectTest.html', form=form, sections=sections)


@app.route('/test2', methods=['POST', 'GET'])
def dateTest():
    form = DateSelect()
    if request.method == 'POST':
        print(form.datePicker.data)
    return render_template('test/calendar_test.html', form=form)


@app.route('/test3/<student>')
def test3(student):
    form = TestSelect()
    return render_template('test/selectTest3.html', student=student, form=form)


@app.route('/enrolled_students/<section>')
def enrolled_student_section(section):
    specific_section = session.execute(select(Sections).where(Sections.name == section)).scalar()
    student_list = specific_section.students
    return render_template('Faculty Website/details-faculty-classes-enrolledstudents.html', section=section, student_list=student_list)


@app.route('/api', methods=['GET', 'POST'])
def test_api():

    current_student = "Vanessa"
    if not os.path.exists(f"{app.config['UPLOAD_FOLDER']}/{current_student}"):
        os.mkdir(f"{app.config['UPLOAD_FOLDER']}/{current_student}")

    if request.method == 'POST':
        if 'image' in request.files:
            images = request.files.getlist('image')
            image_list = []
            for image in images:
                if image.filename != '':
                    #image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                    image_path = f"{app.config['UPLOAD_FOLDER']}/{current_student}/{image.filename}"
                    image.save(image_path)
            return redirect(url_for('test_api_result', cs=current_student))

    return render_template('test/api.html')


@app.route('/api_result/<cs>')
def test_api_result(cs):
    print(cs)
    path = f"{app.config['UPLOAD_FOLDER']}/ref/{cs}"
    files = os.listdir(f"{path}")
    for filename in files:
        print(filename)
    #print(app.config['UPLOAD_FOLDER'], filename)
    #if filename:
    #    image_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    return render_template('test/api_result.html', path=path, filelist=files)

@app.route('/verify')
def api_verify():
    starts = datetime.datetime.now()
    models = [
        "VGG-Face",
        "Facenet",
        "Facenet512",
        "OpenFace",
        "DeepID",
        "ArcFace",
        "SFace",
        "GhostFaceNet",
    ]
    backends = [
        'opencv',
        'ssd',
        'dlib', #
        'mtcnn',
        'fastmtcnn', #
        'retinaface',
        'mediapipe', #
        'yolov8', #
        'yunet',
        'centerface', #
    ]
    sources = ["Elea 1", "Oco 5", "Tugano 4", "t1"]
    results = []
    models=['DeepID']
    #backends=['ssd']
    for i in models:
        a = datetime.datetime.now()
        for source in backends:
            try:
                result = DeepFace.verify(img1_path=f"static/testpic/drew/t1.jpg",
                                         img2_path="static/testpic/Oco/Oco 4.jpg",
                                         model_name=i,
                                         detector_backend=source)
                results.append(result)
                print(i, source, result['verified'])
            except:
                print(f"no face detected using {source}")
            time.sleep(1)
        x = datetime.datetime.now()
        print(f"Time for 1 execution: {x-a}")
    ends = datetime.datetime.now()
    print(f"Took {ends-starts} time to complete.")
    return results

@app.route('/verify2')
def verify2():
    starts = datetime.datetime.now()
    models = [
        "VGG-Face",
        "Facenet",
        "Facenet512",
        "OpenFace",
        "DeepID",
        "ArcFace",
        "SFace",
        "GhostFaceNet",
    ]
    backends = [
        'opencv',
        'ssd',
        'dlib',
        'mtcnn', #?
        'fastmtcnn',
        'retinaface',
        'mediapipe',
        'yolov8',
        'yunet',
        'centerface',
    ]
    result = ""
    try:
        result = DeepFace.verify(img1_path=f"static/testpic/drew/t1.jpg",
                                 img2_path="static/testpic/Elea/Elea 1.jpg",
                                 model_name="DeepID",
                                 detector_backend=backends[2])
        if result['verified'] == True:
            print("WOW")
    except:
        print("No face detected")
    ends = datetime.datetime.now()
    print(f"Took {ends-starts} time to execute. Using {backends[2]} Result: {result}")
    return result


@app.route('/verify3')
def verify3():
    backends = [
        'opencv',
        'ssd',
        'mtcnn',  # ?
        'fastmtcnn',
        'retinaface',
        'mediapipe',
        'yolov8',
        'yunet',
        'centerface',
    ]

    dfs = DeepFace.find(img_path="static/uploads/frame.jpg", db_path="static/testpic", model_name='Facenet512')
    print(dfs)

    # kiosk detects face upon reaching set threshold (92~95?)
    # calls api, parameters = api_key, subject, image

    # mark as present on select activity
    # return result to kiosk
    return "hi"


@app.route('/apitestdrew', methods=['GET'])
def apitestdrew():
    models = [
        "VGG-Face",
        "Facenet",
        "Facenet512",
        "OpenFace",
        "DeepID",
        "ArcFace",
        "SFace",
        "GhostFaceNet",
    ]
    for a in models:
        asd = DeepFace.verify(img1_path='static/uploads/frame.jpg', img2_path='static/testpic/tu/Tugano 1.jpg', model_name=f'{a}')
        print(asd)
    return "hey"


@app.route('/apitestresponse', methods=['POST'])
def apitestresponse():
    file = request.files['file']
    c_id = request.form['text']


    if not os.path.exists(f"{app.config['UPLOAD_FOLDER']}/ATTEMPTS"):
        os.mkdir(f"{app.config['UPLOAD_FOLDER']}/ATTEMPTS")

    len_folder = len(os.listdir(f"{app.config['UPLOAD_FOLDER']}/ATTEMPTS"))

    image_path = f"{app.config['UPLOAD_FOLDER']}/ATTEMPTS/{len_folder}.jpg"
    file.save(image_path)

    try:
        asd = DeepFace.find(img_path=image_path, db_path="static/uploads/ref", model_name='Facenet512', detector_backend='ssd')
        who = asd[0]['identity'][0]
    except:
        return "FAIL"

    print(asd, type(asd))


    directory, filename = os.path.split(who)
    print(f"Directory is {directory}")
    print(f"Filename is {filename}")
    print(f"Test who is {filename.split('.')[0].split(' ')[0]}")
    #who_is = f"{filename.split('.')[0].split(' ')[0:-2]} {filename.split('.')[0].split(' ')[1]}"
    who_is = f"{' '.join(filename.split('.')[0].split(' ')[0:-2])}"

    id_num = filename.split('.')[0].split(' ')[-1]
    try:
        student_id_ind = session.execute(select(Students).where(Students.id_number == id_num)).scalar()
        if student_id_ind.progress >= 50: # Try if working TODO working
            return 'You have already finished the required hours.'
        new_attendance = DaySummary(
            img_proof=image_path,
            date_time=datetime.datetime.now(),
            student_id=student_id_ind.id,
            class_id=c_id
            )
        get_summaries = session.execute(select(DaySummary).where(DaySummary.student_id == student_id_ind.id)).scalars().all()
        today_date = datetime.datetime.now().strftime("%m-%d-%y")
        for summary in get_summaries:  ## try if working TODO 2 working
            if summary.date_time.strftime("%m-%d-%y") == today_date:
                return 'You have already timed in today.'
        progress = (len(get_summaries) + 1) * 2 #hrs, changed from len * 2, to len+1 * 2
        if len(get_summaries) > 0:
            student_id_ind.progress = progress
        else:
            student_id_ind.progress = 2
        session.add(new_attendance)
    except:
        session.rollback()
    session.commit()

    return who_is


@app.route('/csd_admin/register', methods=['POST', 'GET'])
def csd_admin_register_student():
    form = AdminRegisterStudent()
    # TODO modify available sections
    if form.validate_on_submit():
        # register student start
        new_student_role = UserRoles(
            user_id=form.student_number.data,
            user_level=2
        )
        session.add(new_student_role)

        pw = generate_password_hash(form.password.data, method="scrypt")
        new_student_login = LoginInfo(
            user_id=form.student_number.data,
            passwd=pw,
            email=form.email.data
        )
        session.add(new_student_login)

        # put in a try except block, if malicious (added a choice, add to banned ip addresses)
        sec_id = session.execute(select(Sections).where(Sections.name == form.section.data)).scalar()
        sec_id = sec_id.id

        new_student = Students(
            name=f"{form.last_name.data.title()}, {form.first_name.data.title()} {form.middle_name.data.title()}.",
            joindate=datetime.datetime.now(),
            progress=0,
            program=form.course.data,
            sectionid=sec_id,
            id_number=form.student_number.data,
            #student_year=form.year.data
        )
        session.add(new_student)
        try:
            session.commit()
            # create directory for registered student
            current_student = form.student_number.data

            if not os.path.exists(f"{app.config['UPLOAD_FOLDER']}/ref"):
                os.mkdir(f"{app.config['UPLOAD_FOLDER']}/ref")

            if not os.path.exists(f"{app.config['UPLOAD_FOLDER']}/ref/{current_student}"):
                os.mkdir(f"{app.config['UPLOAD_FOLDER']}/ref/{current_student}")

            if 'image' in request.files:
                images = request.files.getlist('image')
                image_list = []
                for i, image in enumerate(images):
                    if image.filename != '':
                        image.filename = f"{form.last_name.data}, {form.first_name.data}"
                        image_path = f"{app.config['UPLOAD_FOLDER']}/ref/{current_student}/{image.filename} {i} {form.student_number.data}.jpg"
                        image.save(image_path)
                        #flash(f'SUCCESSFULLY REGISTERED STUDENT form.student_number.data', 'success')
                return redirect(url_for('test_api_result', cs=current_student))
        except Exception as e:
            session.rollback()
            print("Error:", e)
        #end
    else:
        print(form.errors)
        print(form.section.data)
        for error in form.errors:
            #flash(f"{form.errors[error][0]}", 'error')
            flash(f"{form.errors[error][0]}")
    return render_template('Administrator Website/admin-register-student.html', form=form)


@app.route('/csd_admin/dashboard')
def csd_admin_dashboard():

    # get number of attendance today
    today_date = datetime.datetime.now().strftime("%m-%d-%y")
    today_record = session.execute(select(DaySummary).filter(func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date)).scalars().all()
    how_many_attendances = len(today_record)

    # get available classes
    total_classes = session.execute(select(ClassInfo)).scalars().all()
    how_many_classes = len(total_classes)

    # get number of students
    total_students = session.execute(select(Students)).scalars().all()
    how_many_students = len(total_students)
    return render_template('Administrator Website/admin-dashboard.html', count=how_many_attendances, classes=how_many_classes, students=how_many_students)


@app.route('/csd_admin/available_classes')
def csd_admin_available_classes():
    available_classes = session.execute(select(ClassInfo)).scalars().all()
    return render_template('Administrator Website/admin-classes-availableclasses.html', classes=available_classes)


@app.route('/csd_admin/available_classes/<class_id>')
def csd_admin_available_classes_details(class_id=None):
    # mon, tue, wed, thu, fri, sat
    class_inf = session.execute(select(ClassInfo).where(ClassInfo.id == class_id)).scalar()
    day = class_inf.schedule.day
    grid_col = {
        'M': 'mon',
        'T': 'tue',
        'W': 'wed',
        'TH': 'thu',
        'F': 'fri',
        'S': 'sat'
    }
    time_to_grid_row = {
        "07:00": "h00",
        "07:30": "h01",
        "08:00": "h02",
        "08:30": "h03",
        "09:00": "h04",
        "09:30": "h05",
        "10:00": "h06",
        "10:30": "h07",
        "11:00": "h08",
        "11:30": "h09",
        "12:00": "h10",
        "12:30": "h11",
        "01:00": "h12",
        "01:30": "h13",
        "02:00": "h14",
        "02:30": "h15",
        "03:00": "h16",
        "03:30": "h17",
        "04:00": "h18",
        "04:30": "h19",
        "05:00": "h20",
    }
    grid_name = grid_col.get(day, 'Sunday')
    class_time = class_inf.schedule.time

    start_time, end_time = class_time.split("-")
    if ':' not in start_time:
        start_time += ":00"
    if ':' not in end_time:
        end_time += ":00"
    start_time = start_time.split('PM')[0].split('AM')[0]
    print(start_time)
    start_row = time_to_grid_row.get(start_time, 'h00')
    print(start_row)
    end_r = start_row.split("h")
    s = int(end_r[1]) + 4
    if len(str(s)) == 1:
        end_val = f'0{s}'
    else:
        end_val = f'{s}'
    end_row = f'h{end_val}'
    table_vals = {
        'grid-column': grid_name,
        'grid-row-start': start_row,
        'grid-row-end': end_row
    }
    return render_template('Administrator Website/details-admin-classes-availableclasses.html', table_vals=table_vals, cinfo=class_inf)


@app.route('/csd_admin/enrolled_students')
def csd_admin_enrolled_students():
    available_sections = session.execute(select(Sections)).scalars().all()
    return render_template('Administrator Website/admin-classes-enrolledstudents.html', sections=available_sections)


@app.route('/csd_admin/enrolled_students/<section_id>')
def csd_admin_enrolled_students_details(section_id=None):
    if section_id is None:
        return redirect(url_for('csd_admin_enrolled_students'))
    section_info = session.execute(select(Sections).where(Sections.id == section_id)).scalar()
    section_students = section_info.students
    return render_template('Administrator Website/details-admin-classes-enrolledstudents.html', sinfo=section_info, sstud=section_students)


@app.route('/csd_admin/attendances', methods=['POST', 'GET'])
def csd_admin_attendances():
    form = AdminDailyReport()

    # fill section
    all_sections = session.execute(select(Sections)).scalars().all()
    all_sect = [s.name for s in all_sections]
    form.section.choices += all_sect

    # fill activities
    all_activities = session.execute(select(Activities)).scalars().all()
    all_acts = [act.name for act in all_activities]
    form.activity.choices += all_acts

    # fill faculties
    all_faculties = session.execute(select(Faculty)).scalars().all()
    all_facts = [facul.name for facul in all_faculties]
    form.faculties.choices += all_facts

    # get attendance today
    today_date = datetime.datetime.now().strftime("%m-%d-%y")
    attendances_today = session.execute(select(DaySummary).filter(func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date)).scalars().all()
    # TODO REMOVE FOR TEST ONLY
    #attendances_today = session.execute(select(DaySummary)).scalars().all()
    # enable filtering & sorting
    sec = None if form.section.data == form.section.default else form.section.data
    act = None if form.activity.data == form.activity.default else form.activity.data
    fac = None if form.faculties.data == form.faculties.default else form.faculties.data
    query = "" if form.q.data is None else form.q.data.lower()
    sorted_by = form.sort_by.data

    asda = [ds for ds in attendances_today if (query in ds.student.name.lower()) and
            (sec == ds.class_info.section.name or sec is None) and
            (act == ds.class_info.activity.name or act is None) and
            (fac == ds.class_info.faculty.name or fac is None)]

    test_dic = {
        "Sort_by": sorted(asda, key=lambda asda: asda.date_time, reverse=False),
        "Name": sorted(asda, key=lambda asda: asda.student.name.split(","), reverse=False),
        "Course": sorted(asda, key=lambda asda: asda.student.program, reverse=False),
        "Activity": sorted(asda, key=lambda asda: asda.class_info.activity.name, reverse=False)
    }

    asda = test_dic.get(sorted_by, test_dic["Sort_by"])

    return render_template('Administrator Website/admin-attendance-records.html', form=form, atoday=asda)


@app.route('/csd_admin/attendances/<student_id>')
def csd_admin_attendances_details(student_id):
    student = session.execute(select(Students).where(Students.id_number == student_id)).scalar()
    today_date = datetime.datetime.now().strftime("%m-%d-%y")
    today_record = session.execute(select(DaySummary).filter(and_(DaySummary.student_id == student.id, func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date))).scalars().all()

    # TODO REMOVE, for test only
    #today_record = session.execute(select(DaySummary).where(DaySummary.student_id == student.id)).scalars().all()

    return render_template('Administrator Website/details-admin-attendance-records.html', records=today_record, student=student)


@app.route('/csd_admin/attendance_history', methods=['POST', 'GET'])
def csd_admin_attendance_history():

    form = AdminAttendanceHistory()

    student_list = session.execute(select(Students)).scalars().all()

    # fill section
    all_sections = session.execute(select(Sections)).scalars().all()
    all_sect = [s.name for s in all_sections]
    form.section.choices += all_sect

    # fill faculties
    all_faculties = session.execute(select(Faculty)).scalars().all()
    all_facts = [facul.name for facul in all_faculties]
    form.faculties.choices += all_facts

    # enable filter, query, and sorting
    sec = None if form.section.data == form.section.default else form.section.data
    term = None if form.term.data == form.term.default else form.term.data
    fac = None if form.faculties.data == form.faculties.default else form.faculties.data
    query = "" if form.q.data is None else form.q.data.lower()
    sorted_by = form.sort_by.data

    asda = [ds for ds in student_list if (query in ds.name.lower()) and
            (sec == ds.section.name or sec is None) and
            (fac == ds.section.faculty.name or fac is None)]

    test_dic = {
        "Name": sorted(asda, key=lambda asda: asda.name.split(","), reverse=False),
        "Course": sorted(asda, key=lambda asda: asda.program, reverse=False),
        "Progress": sorted(asda, key=lambda asda: asda.progress, reverse=False)
    }

    asda = test_dic.get(sorted_by, test_dic["Name"])

    term_range = session.execute(select(Term).filter(and_(Term.name == term, Term.start <= datetime.datetime.now(), Term.semester.has(Semester.end >= datetime.datetime.now())))).scalar()

    if term_range:
        valid_data = session.execute(select(DaySummary).filter(and_(DaySummary.date_time >= term_range.start, DaySummary.date_time <= term_range.end))).scalars().all()

        inrange_query = [s.student.id_number for s in valid_data]

        valid_dict = {}

        for asd in asda:
            valid_dict[asd.id_number] = inrange_query.count(asd.id_number) * 2  # multiplied by 2 because each entry is 2hours worth
        print(sec, term, fac, query)
        if 'export_button' in list(request.form):

            data = [{"STUDENT NAME": student.name,
                     "STUDENT NUMBER": student.id_number,
                     "PROGRAM": student.program,
                     "SECTION": student.section.name,
                     "PROGRESS (hrs)": valid_dict.get(student.id_number, 0)
                     } for student in asda]

            df = pd.DataFrame(data)
            file_name = f"ALL_STUDENTS-{form.term.data}-{datetime.datetime.now().strftime('%B%d%Y-%H%M')}"
            df.to_excel(f'{EXCEL_DIRECTORY}/{file_name}.xlsx', index=False)

            # send file to user

            try:
                return send_from_directory(EXCEL_DIRECTORY, f"{file_name}.xlsx", as_attachment=True)
            except:
                return "File does not exist :(", 404

        return render_template('Administrator Website/admin-attendance-history.html', sl=asda, form=form, vd=valid_dict)

    if 'export_button' in list(request.form):
        data = [{"STUDENT NAME": student.name,
                 "STUDENT NUMBER": student.id_number,
                 "PROGRAM": student.program,
                 "SECTION": student.section.name,
                 "PROGRESS (hrs)": student.progress
                 } for student in asda]

        df = pd.DataFrame(data)
        file_name = f"ALL_STUDENTS-FULL_SEMESTER-{datetime.datetime.now().strftime('%B%d%Y-%H%M')}"
        if fac:
            file_name = f"{fac}-{datetime.datetime.now().strftime('%B%d%Y-%H%M')}"
        df.to_excel(f'{EXCEL_DIRECTORY}/{file_name}.xlsx', index=False)

    # send file to user

        try:
            return send_from_directory(EXCEL_DIRECTORY, f"{file_name}.xlsx", as_attachment=True)
        except:
            return "File does not exist :(", 404

    return render_template('Administrator Website/admin-attendance-history.html', form=form, sl=asda)


@app.route('/csd_admin/attendance_history/<student_id>')
def csd_admin_attendance_history_details(student_id):
    s = session.execute(select(Students).where(Students.id_number == student_id)).scalar()
    all_attendances = session.execute(select(DaySummary).where(DaySummary.student_id == s.id)).scalars().all()

    return render_template('Administrator Website/details-admin-attendance-history.html', sinfo=s, attinfo=all_attendances)


@app.route('/csd_admin/archived_attendances')
def csd_admin_archived_attendance():
    # TODO to follow :)
    return render_template('Administrator Website/admin-attendance-archives.html')


@app.route('/csd_admin/manage_faculty', methods=['POST', 'GET'])
def csd_admin_manage_faculty():

    form = AdminManageFaculty()

    query = "" if form.q.data is None else form.q.data.lower()

    all_faculties = session.execute(select(Faculty)).scalars().all()
    faculty_display = [ds for ds in all_faculties if (query in ds.name.lower())]

    faculty_display = sorted(faculty_display, key=lambda faculty_display: faculty_display.name.split(","), reverse=False)

    return render_template('Administrator Website/admin-manage-faculty.html', f=faculty_display, form=form)


@app.route('/csd_admin/manage_faculty/add_faculty', methods=['POST', 'GET'])
def csd_admin_manage_faculty_add():

    form = AdminAddFaculty()

    if request.method == 'POST':

        try:
            # PHASE 1
            new_faculty_role = UserRoles(
                user_id=form.employee_id.data,
                user_level="1"
            )
            session.add(new_faculty_role)

            # PHASE 2
            pw = generate_password_hash(form.password.data, method="scrypt")
            new_faculty_login = LoginInfo(
                user_id=form.employee_id.data,
                passwd=pw,
                email=form.email.data
            )
            session.add(new_faculty_login)

            # PHASE 3
            full_name = f"{form.ln.data}, {form.fn.data} {form.mn.data}."
            new_faculty = Faculty(
                name=full_name,
                id_number=form.employee_id.data
            )
            session.add(new_faculty)

            # try saving
            session.commit()

        except Exception as e:
            print(e)
            session.rollback()

    return render_template('Administrator Website/form-add-faculty.html', form=form)


@app.route('/csd_admin/manage_faculty/<employee_number>/details')
def csd_admin_manage_faculty_details(employee_number):

    form = AdminManageFacultyDetails()

    facinfo = session.execute(select(Faculty).where(Faculty.id_number == employee_number)).scalar()
    fac_classes = facinfo.classes

    return render_template('Administrator Website/details-admin-manage-faculty.html', form=form, f=facinfo, fc=fac_classes)


@app.route('/csd_admin/manage_faculty/edit/<employee_number>')
def csd_admin_manage_faculty_edit(employee_number):
    # TODO Save edited info
    form = AdminEditFaculty()

    faculty_deats = session.execute(select(Faculty).where(Faculty.id_number == employee_number)).scalar()

    if faculty_deats is None:
        return redirect(url_for('csd_admin_manage_faculty'))
    # process name
    name_split = faculty_deats.name.split(",")
    sec_half = name_split[1].strip().split(" ")
    form.ln.data = name_split[0]
    form.mn.data = sec_half[-1]
    form.fn.data = " ".join(sec_half[0:-1])

    form.employee_id.data = faculty_deats.id_number
    form.email.data = faculty_deats.user_role.login_info.email
    form.password.data = "*************"

    return render_template('Administrator Website/form-edit-faculty.html', form=form, fd=faculty_deats)


@app.route('/csd_admin/manage_activity', methods=['POST', 'GET'])
def csd_admin_manage_activity():

    form = AdminManageActivity()
    all_activities = session.execute(select(Activities)).scalars().all()

    query = "" if form.q.data is None else form.q.data.lower()

    all_activities = [ds for ds in all_activities if (query in ds.name.lower())]

    return render_template('Administrator Website/admin-manage-activity.html', acts=all_activities, form=form)


@app.route('/csd_admin/manage_activity/add_activity', endpoint='csd_admin_manage_activity_add', methods=['GET', 'POST'])
def csd_admin_manage_activity_add():
    print(request.method)
    form = AdminAddActivity()

    if form.validate_on_submit():
        new_activity = Activities(
            name=form.aname.data.upper(),
            description=form.adesc.data,
            activity_limit=form.alim.data,
            activity_img=f'static/ACTIMAGES/{form.aname.data.upper()}.jpg'
        )
        session.add(new_activity)

        try:
            session.commit()
            images = request.files.getlist('image')
            for image in images:
                if image.filename != '':
                    image.filename = form.aname.data.upper()
                    image_path = f'static/ACTIMAGES/{image.filename}.jpg'
                    image.save(image_path)
            flash(f'Added new activity: {new_activity.name}', 'success')
        except Exception as e:
            print(e)
            session.rollback()

    else:
        print(form.errors)
    return render_template('Administrator Website/form-add-activity.html', form=form)


@app.route('/csd_admin/manage_activity/<activity_id>/details')
def csd_admin_manage_activity_details(activity_id):
    act_details = session.execute(select(Activities).where(Activities.id == activity_id)).scalar()
    all_instances = session.execute(select(ClassInfo).where(ClassInfo.activity_id == activity_id)).scalars().all()


    return render_template('Administrator Website/details-admin-manage-activity-activityPlan.html', ad=act_details, ais=all_instances)


@app.route('/csd_admin/manage_activity/edit/<activity_id>', endpoint='csd_admin_manage_activity_edit', methods=['GET', 'POST'])
def csd_admin_manage_activity_edit(activity_id):
    # TODO save changes to DB
    form = AdminEditActivity()
    act_details = session.execute(select(Activities).where(Activities.id == activity_id)).scalar()
    if request.method == 'GET':
        form.aid.data = act_details.id
        form.aname.data = act_details.name
        form.adesc.data = act_details.description
        form.alim.data = act_details.activity_limit
        form.aoff.data = act_details.is_offered

    return render_template('Administrator Website/form-edit-activity.html', ad=act_details, form=form)


@app.route('/csd_admin/manage_classes')
def csd_admin_manage_classes():
    # TODO
    all_classes = session.execute(select(ClassInfo)).scalars().all()

    return render_template('Administrator Website/admin-manage-classes.html', ac=all_classes)


@app.route('/csd_admin/manage_classes/add_class', endpoint='csd_admin_manage_classes_add', methods=['GET', 'POST'])
def csd_admin_manage_classes_add():
    form = AdminAddClasses()
    time_start = {
        '1': '7:00AM',
        '2': '7:30AM',
        '3': '8:00AM',
        '4': '8:30AM',
        '5': '9:00AM',
        '6': '9:30AM',
        '7': '10:00AM',
        '8': '10:30AM',
        '9': '11:00AM',
        '10': '11:30AM',
        '11': '12:00PM',
        '12': '12:30PM',
        '13': '1:00PM',
        '14': '1:30PM',
        '15': '2:00PM',
        '16': '2:30PM',
        '17': '3:00PM',
        '18': '3:30PM',
        '19': '4:00PM',
        '20': '4:30PM',
        '21': '5:00PM',
    }

    time_end = {
        '1': '09:00AM',
        '2': '09:30AM',
        '3': '10:00AM',
        '4': '10:30AM',
        '5': '11:00AM',
        '6': '11:30AM',
        '7': '12:00PM',
        '8': '12:30PM',
        '9': '1:00PM',
        '10': '01:30PM',
        '11': '02:00PM',
        '12': '02:30PM',
        '13': '03:00PM',
        '14': '03:30PM',
        '15': '04:00PM',
        '16': '04:30PM',
        '17': '05:00PM',
        '18': '05:30PM',
        '19': '06:00PM',
        '20': '06:30PM',
        '21': '07:00PM',
    }

    # fill activity tab
    activities = session.execute(select(Activities)).scalars().all()
    act_list = [(i.id, i.name) for i in activities]
    form.act_select.choices += act_list

    # fill instructor
    faculties = session.execute(select(Faculty)).scalars().all()
    fac_list = [(f.id, f.name) for f in faculties]
    form.fac_name.choices += fac_list

    if request.method == 'POST':
        print(form.sec_name.data)
        exist_sec = session.execute(select(Sections).where(Sections.name == form.sec_name.data.upper())).scalar()
        if exist_sec:
            flash('This section already has an existing activity')
            return render_template('Administrator Website/form-add-classes.html', form=form)

        sched = session.execute(select(Schedule).filter(and_(Schedule.day == form.day_select.data, Schedule.time == f'{time_start[form.time_select.data]}-{time_end[form.time_select.data]}'))).scalar()

        if exist_sec is None:
            new_section = Sections(
                name=form.sec_name.data.upper(),
                course_code='PATHFIT4',
                facultyid=form.fac_name.data,
            )
            session.add(new_section)
            session.commit()
            section_id = new_section.id

        if sched is None:
            new_schedule = Schedule(
                day=form.day_select.data,
                time=f'{time_start[form.time_select.data]}-{time_end[form.time_select.data]}'
            )
            session.add(new_schedule)
            session.commit()
            schedule_id = new_schedule.id
        else:
            schedule_id = sched.id

        room = 'SRDB'
        facultyid = form.fac_name.data
        activity_id = form.act_select.data

        new_classinfo = ClassInfo(
            room=room,
            facultyid=facultyid,
            activity_id=activity_id,
            schedule_id=schedule_id,
            section_id=section_id
        )
        session.add(new_classinfo)
        try:
            session.commit()
            flash('Successfully added new class', 'success')
        except Exception as e:
            print(e)
            session.rollback()



    return render_template('Administrator Website/form-add-classes.html', form=form)


@app.route('/csd_admin/manage_classes/edit/<class_id>')
def csd_admin_manage_classes_edit(class_id):
    return render_template('Administrator Website/form-edit-classes.html')


@app.route('/csd_admin/manage_students', methods=['POST', 'GET'])
def csd_admin_manage_students():
    form = AdminManageStudent()

    all_students = session.execute(select(Students)).scalars().all()
    query = "" if form.q.data is None else form.q.data.lower()
    fac = None if form.faculties.data == form.faculties.default else form.faculties.data
    sorted_by = form.sort_by.data

    # fill faculties
    all_faculties = session.execute(select(Faculty)).scalars().all()
    all_facts = [facul.name for facul in all_faculties]
    form.faculties.choices += all_facts

    asda = [ds for ds in all_students if (query in ds.name.lower()) and
            (fac == ds.section.faculty.name or fac is None)]

    test_dic = {
        "Select": sorted(asda, key=lambda asda: asda.name.split(","), reverse=False),
        "Name": sorted(asda, key=lambda asda: asda.name.split(","), reverse=False),
        "Course": sorted(asda, key=lambda asda: asda.program, reverse=False),
        "Section": sorted(asda, key=lambda asda: asda.section.name, reverse=False)
    }
    asda = test_dic.get(sorted_by, test_dic["Name"])

    return render_template('Administrator Website/admin-manage-students.html', asd=asda, form=form)


@app.route('/csd_admin/manage_students/add_student')
def csd_admin_manage_students_add():
    return redirect(url_for('csd_admin_register_student'))


@app.route('/csd_admin/manage_students/edit/<student_id>', endpoint='csd_admin_manage_students_edit', methods=['GET', 'POST'])
def csd_admin_manage_students_edit(student_id):

    form = AdminEditStudent()

    selected_student = session.execute(select(Students).where(Students.id_number == student_id)).scalar()

    # prefill with existing data

    # handle name
    try:
        name_split = selected_student.name.split(",")
        sec_half = name_split[1].strip().split(" ")
        form.last_name.data = name_split[0]
        form.middle_name.data = sec_half[-1]
        form.first_name.data = " ".join(sec_half[0:-1])
        full_name = [" ".join(sec_half[0:-1]), sec_half[-1], name_split[0]]

    except:
        full_name = [selected_student.name, '', '']

    if request.method == 'GET':
        form.section.data = selected_student.section.name
        form.course.data = selected_student.program
        form.first_name.data = full_name[0]
        form.middle_name.data = full_name[1]
        form.last_name.data = full_name[2]
        form.email.data = selected_student.user_role.login_info.email
        form.password.data = '*************'

    if request.method == 'POST':
        if form.validate_on_submit():
            get_secid = session.execute(select(Sections).where(Sections.name == form.section.data)).scalar()
            if not get_secid:
                return redirect(url_for('csd_admin_manage_students_edit', student_id=student_id))
            try:
                with session.no_autoflush:

                    session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
                    print(form.middle_name.data)
                    if '.' not in form.middle_name.data:
                        selected_student.name = f"{form.last_name.data.title()}, {form.first_name.data.title()} {form.middle_name.data.title()}."
                    else:
                        selected_student.name = f"{form.last_name.data.title()}, {form.first_name.data.title()} {form.middle_name.data.title()}"

                    s = session.execute(select(UserRoles).where(UserRoles.user_id == student_id)).scalar()
                    slogin = session.execute(select(LoginInfo).where(LoginInfo.user_id == student_id)).scalar()

                    if form.email.data != slogin.email:
                        slogin.email = form.email.data
                    if form.password.data != '*************':
                        slogin.passwd = generate_password_hash(form.password.data)

                    if form.student_number.data != student_id:
                        slogin.user_id = form.student_number.data

                    if form.course.data != selected_student.program:
                        selected_student.program = form.course.data

                    if form.section.data != selected_student.section.id:
                        selected_student.sectionid = get_secid.id


                    selected_student.id_number = form.student_number.data

                    s.user_id = form.student_number.data


                    #selected_student.id_number = form.student_number.data
                    #selected_student.user_role.id_number = form.student_number.data
                    #selected_student.user_role.login_info.id_number = form.student_number.data

                    #selected_student.user_role.login_info.email = form.email.data
                    #selected_student.user_role.login_info.passwd = generate_password_hash(form.password.data)

                    session.commit()
                    session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
                    flash("SUCCESS")
                    return redirect(url_for('csd_admin_manage_students'))
            except Exception as e:
                print(e)
                session.rollback()
        else:
            print(form.errors)

    return render_template('Administrator Website/form-edit-student.html', student=selected_student, form=form, names=full_name)


if __name__ == '__main__':
    #app.run(host='26.252.8.101', port=5000, debug=True)
    #app.run(host='172.24.165.146', port=5000, debug=True)
    #app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)




    