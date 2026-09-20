from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    """Base account used for login for ALL roles (student, faculty, admin)."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student | faculty | admin
    full_name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
    faculty = db.relationship("Faculty", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "full_name": self.full_name,
            "is_active": self.is_active,
        }


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(255))

    courses = db.relationship("Course", backref="department", cascade="all, delete-orphan")
    students = db.relationship("Student", backref="department")
    faculty = db.relationship("Faculty", backref="department")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "total_students": len(self.students),
            "total_courses": len(self.courses),
        }


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    duration_years = db.Column(db.Integer, default=4)
    description = db.Column(db.String(255))

    subjects = db.relationship("Subject", backref="course", cascade="all, delete-orphan")
    students = db.relationship("Student", backref="course")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "duration_years": self.duration_years,
            "description": self.description,
        }


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=True)
    semester = db.Column(db.Integer, default=1)
    credits = db.Column(db.Integer, default=3)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "course_id": self.course_id,
            "course_name": self.course.name if self.course else None,
            "faculty_id": self.faculty_id,
            "faculty_name": self.faculty_ref.user.full_name if self.faculty_id and self.faculty_ref else None,
            "semester": self.semester,
            "credits": self.credits,
        }


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_id = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    dob = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    year = db.Column(db.Integer, default=1)
    cgpa = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendance_records = db.relationship("Attendance", backref="student", cascade="all, delete-orphan")
    marks_records = db.relationship("Marks", backref="student", cascade="all, delete-orphan")
    assignment_submissions = db.relationship("AssignmentSubmission", backref="student", cascade="all, delete-orphan")
    fees = db.relationship("Fee", backref="student", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "student_id": self.student_id,
            "full_name": self.user.full_name if self.user else None,
            "email": self.user.email if self.user else None,
            "phone": self.phone,
            "dob": self.dob,
            "gender": self.gender,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "course_id": self.course_id,
            "course_name": self.course.name if self.course else None,
            "year": self.year,
            "cgpa": self.cgpa,
        }


class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    faculty_id = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    designation = db.Column(db.String(80), default="Assistant Professor")
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subjects = db.relationship("Subject", backref="faculty_ref")
    assignments = db.relationship("Assignment", backref="faculty", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "faculty_id": self.faculty_id,
            "full_name": self.user.full_name if self.user else None,
            "email": self.user.email if self.user else None,
            "phone": self.phone,
            "designation": self.designation,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
        }


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")
    student = db.relationship("Student")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
        }


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present | Absent

    subject = db.relationship("Subject")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
            "date": self.date,
            "status": self.status,
        }


class Marks(db.Model):
    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    internal = db.Column(db.Float, default=0)
    external = db.Column(db.Float, default=0)

    subject = db.relationship("Subject")

    @property
    def total(self):
        return round((self.internal or 0) + (self.external or 0), 2)

    @property
    def grade(self):
        t = self.total
        if t >= 90: return "A+"
        if t >= 80: return "A"
        if t >= 70: return "B+"
        if t >= 60: return "B"
        if t >= 50: return "C"
        if t >= 40: return "D"
        return "F"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
            "internal": self.internal,
            "external": self.external,
            "total": self.total,
            "grade": self.grade,
        }


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")
    submissions = db.relationship("AssignmentSubmission", backref="assignment", cascade="all, delete-orphan")

    def to_dict(self, student_id=None):
        status = "Pending"
        if student_id:
            sub = next((s for s in self.submissions if s.student_id == student_id), None)
            if sub:
                status = sub.status
        return {
            "id": self.id,
            "title": self.title,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
            "due_date": self.due_date,
            "description": self.description,
            "status": status,
        }


class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    status = db.Column(db.String(20), default="Submitted")
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    audience = db.Column(db.String(20), default="all")  # all | student | faculty
    posted_by = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "audience": self.audience,
            "posted_by": self.posted_by,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


class Fee(db.Model):
    __tablename__ = "fees"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    semester = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float, default=0)
    due_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Unpaid")

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "semester": self.semester,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "balance": round(self.total_amount - self.paid_amount, 2),
            "due_date": self.due_date,
            "status": self.status,
        }


class Timetable(db.Model):
    __tablename__ = "timetable"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"))
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    room = db.Column(db.String(30))

    subject = db.relationship("Subject")
    course = db.relationship("Course")
    faculty = db.relationship("Faculty")

    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "course_name": self.course.name if self.course else None,
            "subject_id": self.subject_id,
            "subject_name": self.subject.name if self.subject else None,
            "faculty_name": self.faculty.user.full_name if self.faculty and self.faculty.user else None,
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "room": self.room,
        }
