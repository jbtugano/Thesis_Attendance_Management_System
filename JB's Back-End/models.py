from sqlalchemy import (Column, Integer, String, DateTime, SmallInteger, ForeignKey, Boolean,
                        Table, select)
from sqlalchemy.orm import declarative_base, relationship
from db import engine
from flask_login import UserMixin

Base = declarative_base()


# TODO add day summary, attendance log

student_class = Table('student_cinfo', Base.metadata,
    Column('classinfo_id', Integer, ForeignKey('classinfo.id')),
    Column('student_id', Integer, ForeignKey('students.id'))
)


class Students(Base):

    __tablename__ = "students"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    joindate = Column(DateTime, nullable=False)
    progress = Column(SmallInteger, nullable=True)
    program = Column(String(50), nullable=False)

    #relationship with faceid table 1t1
    face_id = relationship("FaceId", uselist=False, back_populates="student")

    #relationship with sections mt1
    sectionid = Column(Integer, ForeignKey("section.id"))
    section = relationship("Sections", back_populates="students")

    #relationship with classinfo mtm
    #classes = relationship("ClassInfo", secondary=student_class, back_populates="students")

    #relationship with userroles
    id_number = Column(String(50), ForeignKey("userrole.user_id")) #student id number
    user_role = relationship('UserRoles', back_populates="students")

class FaceId(Base):

    __tablename__ = "faceid"

    id = Column(Integer, autoincrement=True, primary_key=True)
    faceid = Column(String(50), nullable=False) #to change

    #relationship with students table
    studentid = Column(Integer, ForeignKey('students.id'))
    student = relationship("Students", back_populates="face_id")


class Faculty(Base):

    __tablename__ = "faculty"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)


    #relationship with section

    sections = relationship("Sections", back_populates="faculty")

    #relationship with classinfo
    classes = relationship("ClassInfo", back_populates="faculty")

    #relationship with userrole
    id_number = Column(String(50), ForeignKey("userrole.user_id"))
    user_role = relationship('UserRoles', back_populates="faculties")


class Sections(Base):
# TODO consider removing sections bc students are not bound to a professor/section but is nice to know adviser/group by section
    __tablename__ = "section"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(15), nullable=False)
    course_code = Column(String(50), nullable=False) #subject code

    #relationship with faculty
    facultyid = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship("Faculty", back_populates="sections")

    #relationship with student
    students = relationship("Students", back_populates="section")

    # classinfo
    sec_class = relationship("ClassInfo", back_populates="section")


class Activities(Base):

    __tablename__ = "activity"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    #activity_plan = Column(String(100), nullable=True)
    activity_img = Column(String(50), nullable=True)
    activity_limit = Column(SmallInteger, nullable=True) #if none = 40
    is_offered = Column(Boolean, nullable=True, default=1) #if none =  true


class ClassInfo(Base):

    __tablename__ = "classinfo"

    id = Column(Integer, autoincrement=True, primary_key=True)
    room = Column(String(50), nullable=True)


    #relationship with faculty
    facultyid = Column(Integer, ForeignKey("faculty.id"))
    faculty = relationship("Faculty", back_populates="classes")

    # students mtm
    #students = relationship("Students", secondary=student_class, back_populates="classes")

    # activity
    activity_id = Column(Integer, ForeignKey("activity.id"))
    activity = relationship("Activities")

    #  time period
    schedule_id = Column(Integer, ForeignKey("schedule.id"))
    schedule = relationship("Schedule", back_populates="classes")

    # section
    section_id = Column(Integer, ForeignKey("section.id"))
    section = relationship("Sections", back_populates="sec_class")

class Schedule(Base):

    __tablename__ = "schedule"

    id = Column(Integer, autoincrement=True, primary_key=True)
    day = Column(String(5), nullable=False)
    time = Column(String(15), nullable=False)
    "1:30-5:30"
    #relationship with class
    classes = relationship("ClassInfo", back_populates="schedule")


class LoginInfo(UserMixin, Base):

    __tablename__ = "logininfo"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(50), ForeignKey("userrole.user_id"), unique=True, nullable=False)
    passwd = Column(String(200), nullable=False)
    email = Column(String(50), nullable=True)

    #relationship with userrole
    user_role = relationship("UserRoles", back_populates="login_info")


class UserRoles(Base):

    __tablename__ = "userrole"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(50), unique=True, nullable=False)
    user_level = Column(SmallInteger, nullable=False)


    #relationship with Student
    students = relationship("Students", uselist=False, back_populates="user_role")

    #relationship with Faculty
    faculties = relationship("Faculty", uselist=False, back_populates="user_role")

    #relationship with login info
    login_info = relationship("LoginInfo", uselist=False, back_populates="user_role")


class DaySummary(Base):

    __tablename__ = "daysummary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_proof = Column(String(100), nullable=False)
    date_time = Column(DateTime, nullable=False)

    #relationship with Student
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Students")

    #relationship with ClassInfo
    class_id = Column(Integer, ForeignKey("classinfo.id"))
    class_info = relationship("ClassInfo")

Base.metadata.create_all(engine)



#new_act = Activities(
#    name="TEST2"
#                    )
#
#session.add(new_act)
#session.commit()

#x = session.execute(select(Activities).where(Activities.id == 5)).scalar()


zxc = ""
#zxc = input(":")
if zxc == "a":
    #Base.metadata.reflect(bind=engine)
    print(zxc)
    Base.metadata.drop_all(bind=engine)

elif zxc == "b":
    pass
