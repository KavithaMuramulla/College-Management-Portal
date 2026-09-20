"""
Run this once to create the database tables and populate demo data.
Usage:  python seed.py
"""
from datetime import datetime, timedelta
from app import create_app
from extensions import db
from models import (
    User, Student, Faculty, Department, Course, Subject,
    Attendance, Marks, Assignment, Notice, Fee, Timetable
)

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ---------------- Departments ----------------
    cse = Department(name="Computer Science & Engineering", code="CSE", description="Software, AI and systems.")
    ece = Department(name="Electronics & Communication", code="ECE", description="Circuits, signals and communication.")
    mech = Department(name="Mechanical Engineering", code="MECH", description="Design, manufacturing and thermal systems.")
    db.session.add_all([cse, ece, mech])
    db.session.flush()

    # ---------------- Courses ----------------
    btech_cse = Course(name="B.Tech Computer Science", code="BT-CSE", department_id=cse.id, duration_years=4,
                        description="A comprehensive program in computer science and engineering.")
    btech_ece = Course(name="B.Tech Electronics", code="BT-ECE", department_id=ece.id, duration_years=4,
                        description="Focused on electronics and communication systems.")
    btech_mech = Course(name="B.Tech Mechanical", code="BT-MECH", department_id=mech.id, duration_years=4,
                         description="Core mechanical engineering principles and design.")
    db.session.add_all([btech_cse, btech_ece, btech_mech])
    db.session.flush()

    # ---------------- Admin ----------------
    admin_user = User(email="admin@novatech.edu", role="admin", full_name="Nova Admin")
    admin_user.set_password("Admin@123")
    db.session.add(admin_user)

    # ---------------- Faculty ----------------
    fac_user1 = User(email="rjames@novatech.edu", role="faculty", full_name="Dr. Rachel James")
    fac_user1.set_password("Faculty@123")
    db.session.add(fac_user1)
    db.session.flush()
    faculty1 = Faculty(user_id=fac_user1.id, faculty_id="FAC-1001", phone="9876543210",
                        designation="Associate Professor", department_id=cse.id)
    db.session.add(faculty1)

    fac_user2 = User(email="mkhan@novatech.edu", role="faculty", full_name="Prof. Michael Khan")
    fac_user2.set_password("Faculty@123")
    db.session.add(fac_user2)
    db.session.flush()
    faculty2 = Faculty(user_id=fac_user2.id, faculty_id="FAC-1002", phone="9876543211",
                        designation="Assistant Professor", department_id=cse.id)
    db.session.add(faculty2)
    db.session.flush()

    # ---------------- Subjects ----------------
    subj_dsa = Subject(name="Data Structures & Algorithms", code="CSE201", course_id=btech_cse.id,
                        faculty_id=faculty1.id, semester=3, credits=4)
    subj_dbms = Subject(name="Database Management Systems", code="CSE202", course_id=btech_cse.id,
                         faculty_id=faculty1.id, semester=3, credits=4)
    subj_os = Subject(name="Operating Systems", code="CSE203", course_id=btech_cse.id,
                       faculty_id=faculty2.id, semester=4, credits=3)
    subj_ai = Subject(name="Artificial Intelligence", code="CSE301", course_id=btech_cse.id,
                       faculty_id=faculty2.id, semester=5, credits=4)
    db.session.add_all([subj_dsa, subj_dbms, subj_os, subj_ai])
    db.session.flush()

    # ---------------- Students ----------------
    students_data = [
        ("Ava Thompson", "NTU2024001", "ava.thompson@novatech.edu", "Female"),
        ("Liam Carter", "NTU2024002", "liam.carter@novatech.edu", "Male"),
        ("Sophia Martinez", "NTU2024003", "sophia.martinez@novatech.edu", "Female"),
    ]
    student_objs = []
    for name, sid, email, gender in students_data:
        u = User(email=email, role="student", full_name=name)
        u.set_password("Student@123")
        db.session.add(u)
        db.session.flush()
        s = Student(user_id=u.id, student_id=sid, phone="9000000000", dob="2004-05-12",
                    gender=gender, department_id=cse.id, course_id=btech_cse.id, year=2, cgpa=8.4)
        db.session.add(s)
        db.session.flush()
        student_objs.append(s)

    main_student = student_objs[0]

    # ---------------- Attendance (demo, last 15 days) ----------------
    for i in range(15):
        date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        for subj in [subj_dsa, subj_dbms, subj_os]:
            status = "Present" if i % 4 != 0 else "Absent"
            db.session.add(Attendance(student_id=main_student.id, subject_id=subj.id, date=date_str, status=status))

    # ---------------- Marks ----------------
    db.session.add(Marks(student_id=main_student.id, subject_id=subj_dsa.id, internal=28, external=58))
    db.session.add(Marks(student_id=main_student.id, subject_id=subj_dbms.id, internal=25, external=52))
    db.session.add(Marks(student_id=main_student.id, subject_id=subj_os.id, internal=22, external=48))

    # ---------------- Assignments ----------------
    a1 = Assignment(title="Binary Search Tree Implementation", subject_id=subj_dsa.id, faculty_id=faculty1.id,
                     due_date=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                     description="Implement a self-balancing BST in C++ or Python.")
    a2 = Assignment(title="Normalization Case Study", subject_id=subj_dbms.id, faculty_id=faculty1.id,
                     due_date=(datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                     description="Normalize the given schema up to BCNF.")
    db.session.add_all([a1, a2])

    # ---------------- Notices ----------------
    db.session.add(Notice(title="Mid-Semester Exams Schedule Released",
                           content="The mid-semester examination timetable has been published on the notice board. Please check your respective department pages.",
                           audience="student", posted_by="Examination Cell"))
    db.session.add(Notice(title="Faculty Development Program",
                           content="A 3-day Faculty Development Program on AI in Education will be held starting next Monday.",
                           audience="faculty", posted_by="Administration"))
    db.session.add(Notice(title="Annual Tech Fest - Innovate 2026",
                           content="Nova Tech University proudly announces Innovate 2026, our annual technical festival, featuring hackathons, robotics and guest lectures.",
                           audience="all", posted_by="Administration"))

    # ---------------- Fees ----------------
    db.session.add(Fee(student_id=main_student.id, semester=3, total_amount=85000, paid_amount=85000,
                        due_date="2026-08-01", status="Paid"))
    db.session.add(Fee(student_id=main_student.id, semester=4, total_amount=85000, paid_amount=40000,
                        due_date="2026-12-15", status="Partial"))

    # ---------------- Timetable ----------------
    schedule = [
        (subj_dsa, "Monday", "09:00", "10:00", "Room 101"),
        (subj_dbms, "Monday", "10:15", "11:15", "Room 102"),
        (subj_os, "Tuesday", "09:00", "10:00", "Room 101"),
        (subj_ai, "Wednesday", "11:00", "12:00", "Lab 3"),
        (subj_dsa, "Thursday", "09:00", "10:00", "Room 101"),
        (subj_dbms, "Friday", "10:15", "11:15", "Room 102"),
    ]
    for subj, day, start, end, room in schedule:
        db.session.add(Timetable(course_id=btech_cse.id, subject_id=subj.id, faculty_id=subj.faculty_id,
                                  day=day, start_time=start, end_time=end, room=room))

    db.session.commit()

    print("=" * 60)
    print("Nova Tech University database seeded successfully!")
    print("=" * 60)
    print("Admin login:    admin@novatech.edu   / Admin@123")
    print("Faculty login:  rjames@novatech.edu  / Faculty@123")
    print("Student login:  ava.thompson@novatech.edu / Student@123")
    print("=" * 60)
