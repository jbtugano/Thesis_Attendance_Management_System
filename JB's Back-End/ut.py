from db import Session
from models import Schedule, ClassInfo, Activities, Sections, Faculty, UserRoles, Students, LoginInfo, DaySummary
from sqlalchemy import select
import datetime
import random
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


generate_attendance()