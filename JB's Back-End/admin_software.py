import tkinter
import tkinter as tk
from models import Sections, Faculty, Activities, FaceId, Schedule, ClassInfo, Students
from db import Session, select


main = tk.Tk()
session = Session()
#remove default windows control
main.overrideredirect(True)

#app window size
appx = 1280
appy = 720

#get center of screen height, width
x = main.winfo_screenwidth() // 2
y = main.winfo_screenheight() // 2

#center of screen relative to app size
screen_mid_x = x - ( appx // 2)
screen_mid_y = y - ( appy // 2)

#window size and placement
main.geometry(f"{appx}x{appy}+{screen_mid_x}+{screen_mid_y}")

frame = tk.Frame(main, bg="red", height=(appy//6))
frame.pack(fill="x")


# add section
def add_section(name, course_code, faculty):
    new_section = Sections(
        name=name,
        course_code=course_code,
        facultyid=faculty
    )
    session.add(new_section)
    session.commit()


# add faculty
def add_faculty(name, user_id):
    new_faculty = Faculty(
        name=name,
        id_number=user_id
    )
    session.add(new_faculty)
    session.commit()


# add activity
def add_activity(name,
                 description="",
                 activity_img="",
                 activity_limit=40,
                 is_offered=1):

    new_activity = Activities(
        name=name,
        description=description,
        activity_img=activity_img,
        activity_limit=activity_limit,
        is_offered=is_offered

    )
    session.add(new_activity)
    session.commit()


# bind faceid to student
def register_faceid(
                    studentid,
                    faceid=""
                    ):

    new_face_data = FaceId(
        faceid=faceid,
        studentid=studentid
    )
    session.add(new_face_data)
    session.commit()


# add sched
def add_schedule(day="M", time="XX:XX-XX:XX"):
    new_sched = Schedule(
        day=day,
        time=time
    )
    session.add(new_sched)
    session.commit()


# add classinfo
def add_class(room="SRDB",
              facultyid=0,
              activity_id=0,
              schedule_id=0):

    new_class = ClassInfo(
        room=room,
        facultyid=facultyid,
        activity_id=activity_id,
        schedule_id=schedule_id
    )
    session.add(new_class)
    session.commit()


# import excel file
def import_excel():
    # TODO
    """
    check for faculty first

    -if faculty is not in db,   (FACULTY)
    prompt for choice: add or skip to next entry

    -next add section, dependent on faculty (SECTION + SUBJECT CODE)
    the faculty in same row will be the adviser for this section

    -check if activity already exists, if not add to db (SUBJECT MATTER)

    -add class info:
     -> pre-req: pt1, pt2, pt3, incl date time + room here



    """

    pass


# view students
def display_students():
    students = session.execute(select(Students)).scalars().all()
    # TODO create a loop to display all active students


# view faculty
def display_faculty():
    faculties = session.execute(select(Faculty)).scalars().all()
    # TODO create a loop to display all professors


# view activities
def display_activities():
    activities = session.execute(select(Activities)).scalars().all()
    # TODO create a loop in table to display actvities


# view schedules
def display_schedule():
    schedules = session.execute(select(Schedule)).scalars().all()
    # TODO create an algorithm to display schedule


def get_data():
    name = act_name.get()
    desc = act_description.get()
    img_url = act_img.get()
    limit = int(act_limit.get())
    is_active = int(act_status.get())
    add_activity(name=name,
                 description=desc,
                 activity_img=img_url,
                 activity_limit=limit,
                 is_offered=is_active
                 )


name_frame = tk.Frame(main)
name_frame.pack()

test_label = tk.Label(name_frame, text="Activity Name: ")
test_label.pack(side=tk.LEFT)

act_name = tk.Entry(name_frame)
act_name.pack(side=tk.LEFT)

desc_frame = tk.Frame(main)
desc_frame.pack()

desc_label = tk.Label(desc_frame, text="Activity Description: ")
desc_label.pack(side=tk.LEFT)

act_description = tk.Entry(desc_frame)
act_description.pack(side=tk.LEFT)

img_frame = tk.Frame(main)
img_frame.pack()

img_label = tk.Label(img_frame, text="Activity IMAGE URL: ")
img_label.pack(side=tk.LEFT)

act_img = tk.Entry(img_frame)
act_img.pack(side=tk.LEFT)

limit_frame = tk.Frame(main)
limit_frame.pack()

limit_label = tk.Label(limit_frame, text="Student Limit: ")
limit_label.pack(side=tk.LEFT)

act_limit = tk.Entry(limit_frame)
act_limit.pack(side=tk.LEFT)

status_frame = tk.Frame(main)
status_frame.pack()

status_label = tk.Label(status_frame, text="Currently Offering Activity?")
status_label.pack(side=tk.LEFT)

act_status = tk.Entry(status_frame)
act_status.pack(side=tk.LEFT)

framea = tk.Button(main, bg="green", text="CREATE ACTIVITY", command=lambda: get_data())
framea.pack()






main.mainloop()
