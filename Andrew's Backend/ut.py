from db import Session
from models import Schedule, ClassInfo, Activities, Sections, Faculty, UserRoles, Students, LoginInfo, DaySummary, AcademicYear, Semester, Term
from sqlalchemy import select, and_, func
import datetime
import random
import os
import pandas as pd
import time
import math
#from deepface import DeepFace
from werkzeug.security import generate_password_hash, check_password_hash
session = Session()

days = ["M", "T", "W", "TH", "F", "S"]
user_levels = {
    "student": 2,
    "faculty": 1,
    "admin": 0
}
#for day in days:
#    new_time = Schedule(
#        day=day,
#        time="12-2"
#    )
#    session.add(new_time)
#    session.commit()


def generate_activities(number):
    for i in range(number):
        new_activity = Activities(
            name=f"act{i}"
        )
        session.add(new_activity)
    session.commit()


def generate_faculty(number, name):
    #for i in range(number):
    new_faculty_role = UserRoles(
        user_id=number,
        user_level="1"
    )
    session.add(new_faculty_role)


    new_faculty_login = LoginInfo (
        user_id=new_faculty_role.user_id,
        passwd="testc",
        email="testc@gmail.com"
    )
    session.add(new_faculty_login)

    new_faculty = Faculty(
        name=name,
        id_number=new_faculty_role.user_id
    )
    session.add(new_faculty)

    session.commit()


courses = ['CompSci', 'Compu123', 'CivilEng', 'IT', 'Tourism']
def generate_student(number, sectionid):
    x = random.randint(0, 99)
    new_student_role = UserRoles(
        user_id=number,
        user_level=user_levels["student"]
    )
    session.add(new_student_role)


    new_student_login = LoginInfo(
        user_id=new_student_role.user_id,
        passwd=f"testb{x}",
        email=f"testb{x}@gmail.com"
    )
    session.add(new_student_login)


    new_student = Students(
        name=f"drew{x}",
        joindate=datetime.datetime.now(),
        progress=99,
        program=random.choice(courses),
        sectionid=sectionid,
        id_number=new_student_role.user_id
    )
    session.add(new_student)

    session.commit()


def generate_section(name, facultyid, course_code="PATHFIT 4"):
    new_section = Sections(
        name=name,
        course_code=course_code,
        facultyid=facultyid
    )
    session.add(new_section)
    session.commit()


def generate_classinfo():
    new_classInfo = ClassInfo(
        room='SRDB',
        facultyid=1,
        activity_id=random.randint(1, 9),
        schedule_id=random.randint(1, 3),
        section_id=1
    )
    session.add(new_classInfo)
    session.commit()


def generate_attendance():
    new_attendance = DaySummary(
        img_proof='',
        date_time=datetime.datetime.now(),
        student_id=7,
        class_id=3

    )
    session.add(new_attendance)
    session.commit()

# GET CLASSES TO DISPLAY

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
        'mtcnn', #?
        'yunet',
        'centerface',
    ]

"""
backends = ['ssd']
for model in models:
    for backend in backends:
        start = datetime.datetime.now()
        s = DeepFace.find(
            img_path='static/uploads/ATTEMPTS/34.jpg',
            db_path='static/uploads/Vanessa',
            model_name=model,
            detector_backend=backend
                          )
        end = datetime.datetime.now()
        print(f"MODEL: {model} - BACKEND: {backend} - TOOK {end - start} - RESULT: {s} ")
        print("---------------------------------------------------------")
        time.sleep(1)
"""


def add_academic_year(year, start, end):

    new_academic_year = AcademicYear(
        year=year,
        start=start,
        end=end,
    )
    session.add(new_academic_year)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()


def add_semester(name, start, end, acadyear_id):

    new_semester = Semester(
        name=name,
        start=start,
        end=end,
        academic_year_id=acadyear_id,
    )
    session.add(new_semester)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()


def add_term(name, start, end, sem_id):

    new_term = Term(
        name=name,
        start=start,
        end=end,
        semester_id=sem_id,
    )
    session.add(new_term)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()


#add_academic_year("2324",)

#semesters
first_sem_s = datetime.datetime(2023, 8, 22)
first_sem_e = datetime.datetime(2024, 1, 24)
second_sem_s = datetime.datetime(2024, 2, 12)
second_sem_e = datetime.datetime(2024, 6, 17)
special_s = datetime.datetime(2024, 7, 1)
special_e = datetime.datetime(2024, 8, 19)


#terms
fsprelim_s = datetime.datetime(2023, 8, 22)
fsprelim_e = datetime.datetime(2023, 9, 26)

fsmidterm_s = datetime.datetime(2023, 9, 27)
fsmidterm_e = datetime.datetime(2023, 11, 14)

fsfinal_s = datetime.datetime(2023, 11, 15)
fsfinal_e = datetime.datetime(2024, 1, 9)
#------------------------------------------------------------------------------
ssprelim_s = datetime.datetime(2024, 2, 12)
ssprelim_e = datetime.datetime(2024, 3, 16)

ssmidterm_s = datetime.datetime(2024, 3, 17)
ssmidterm_e = datetime.datetime(2024, 4, 27)

ssfinal_s = datetime.datetime(2024, 4, 28)
ssfinal_e = datetime.datetime(2024, 6, 15)
#------------------------------------------------------------------------------
spmidterm_s = datetime.datetime(2024, 7, 1)
spmidterm_e = datetime.datetime(2024, 7, 20)

spfinal_s = datetime.datetime(2024, 7, 21)
spfinal_e = datetime.datetime(2024, 8, 10)


#add_semester(name="1st Semester", start=first_sem_s, end=first_sem_e, acadyear_id=1)
#add_semester(name="2nd Semester", start=second_sem_s, end=second_sem_e, acadyear_id=1)
#add_semester(name="Special Semester", start=special_s, end=special_e, acadyear_id=1)

#add_term(name="Prelim", start=fsprelim_s, end=fsprelim_e, sem_id=1)
#add_term(name="Midterm", start=fsmidterm_s, end=fsmidterm_e, sem_id=1)
#add_term(name="Finals", start=fsfinal_s, end=fsfinal_e, sem_id=1)

#add_term(name="Prelim", start=ssprelim_s, end=ssprelim_e, sem_id=2)
#add_term(name="Midterm", start=ssmidterm_s, end=ssmidterm_e, sem_id=2)
#add_term(name="Finals", start=ssfinal_s, end=ssfinal_e, sem_id=2)

#add_term(name="Midterm", start=spmidterm_s, end=spmidterm_e, sem_id=3)
#add_term(name="Finals", start=spfinal_s, end=spfinal_e, sem_id=3)



#aasd = session.execute(select(Term)).scalars().all()
#for i in aasd:
#    print(i.semester.end)
# TODO for excel reading
"""
asd = "2022-2-02467"
name = "DE ADA, ISAAC KURT RUDY GARCIA"
name_split = name.split(" ")
print(name, name_split)
print(asd)
x = asd.split("-")[-1]
print(len(x)) """


"""name = "DE ADA, ISAAC KURT RUDY GARCIA"
name_split = name.split(",")
sec_half = name_split[1].strip().split(" ")
ln = name_split[0]
mn = sec_half[-1]
fn = " ".join(sec_half[0:-1])
print(f"{ln}, {fn} {mn}.")"""


'2024-2-44267'


def add_classes():

    s = session.execute(select(Sections).where(Sections.name == 'inputted section')).scalar()
    sched = session.execute(select(Schedule).filter(and_(Schedule.day == 'selected day', Schedule.time == 'selected time'))).scalar()
    if s is None:
        new_section = Sections(
            name='',
            course_code='PATHFIT4',
            facultyid=f.id,
        )
        session.add(new_section)
    if sched is None:
        new_schedule = Schedule(
            day='selected day',
            time='selected time'
        )
    room = 'SRDB'
    facultyid = f.facultyid
    activity_id = activity.id



    pass

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
    '1': '9:00AM',
    '2': '9:30AM',
    '3': '10:00AM',
    '4': '10:30AM',
    '5': '11:00AM',
    '6': '11:30AM',
    '7': '12:00PM',
    '8': '12:30PM',
    '9': '1:00PM',
    '10': '1:30PM',
    '11': '2:00PM',
    '12': '2:30PM',
    '13': '3:00PM',
    '14': '3:30PM',
    '15': '4:00PM',
    '16': '4:30PM',
    '17': '5:00PM',
    '18': '5:30PM',
    '19': '6:00PM',
    '20': '6:30PM',
    '21': '7:00PM',
}

# get daysummary time today
'''  
today_date = datetime.datetime.now().strftime("%m-%d-%y")
attendances_today = session.execute(select(DaySummary).filter(func.date_format(DaySummary.date_time, "%m-%d-%y") == today_date)).scalars().all()
print(attendances_today) '''

'''
models = [
    'VGG-Face',
    'Facenet',
    'Facenet512',
    'DeepID'
]
metrics = [
    'cosine',
    'euclidean',
    'euclidean_l2'
]
directory_path = 'static/uploads'
sources = os.listdir(f'{directory_path}/measured_data')

whole_start = datetime.datetime.now()
not_founds = 0
all_distance = 0
for s in sources:
    start = datetime.datetime.now()
    asd = DeepFace.find(img_path=f'{directory_path}/measured_data/{s}', db_path=f'{directory_path}/copied_ref',
                        model_name=models[3], detector_backend='ssd', distance_metric=metrics[2])          # Cosine Similarity - Euclidean - Euclidean_l2
    end = datetime.datetime.now()
    try:
        who = asd[0]['identity'][0]
        dist = asd[0]['distance'][0]
        all_distance += dist
    except:
        who = 'NOT FOUND'
        dist = 'NONE'
        not_founds += 1
    print(f"Processed {s}, took {end - start}, identified as {who}, {dist}")
    print('-------------------------------------------------------')
whole_end = datetime.datetime.now()

print(f'Processed 30 images, took {whole_end-whole_start}, not_founds={not_founds}, ave_distance={all_distance/(30-not_founds)}')
'''

s = session.execute(select(Schedule).where(Schedule.id == 5)).scalar()
print(s.time)
s.time = '07:00AM-09:00AM'
print(s.time)
session.commit()