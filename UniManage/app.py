"""
UniManage – Flask Application
=============================
Run: python app.py
"""
import os, uuid, io, csv
from datetime import date
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, jsonify, session, Response
)
from config import config_map

app = Flask(__name__)
app.config.from_object(config_map["development"])
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ── User Authentication Configuration ───────────────────────────
DEMO_USERS = {
    "admin@unimanage.edu": {
        "password": "admin123",
        "name": "Prof. David Miller",
        "role": "System Administrator",
        "avatar": "AD",
        "email": "admin@unimanage.edu"
    },
    "faculty@unimanage.edu": {
        "password": "faculty123",
        "name": "Dr. Sarah Jenkins",
        "role": "Dean of Academic Affairs",
        "avatar": "SJ",
        "email": "faculty@unimanage.edu"
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in to access the university dashboard.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    return {
        "current_user": session.get("user", {
            "name": "Prof. David Miller",
            "role": "System Administrator",
            "avatar": "AD",
            "email": "admin@unimanage.edu"
        })
    }

# ── Academic Departments ────────────────────────────────────────
DEPARTMENTS = [
    "Computer Science", "Information Technology", "Software Engineering",
    "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
    "Business Administration", "Economics", "Mathematics", "Physics",
    "Chemistry", "Biology", "Medical Science", "Law", "Architecture"
]

# ── Courses Database ────────────────────────────────────────────
courses_db = [
    {"id": "1", "code": "CS101", "title": "Introduction to Computer Science", "department": "Computer Science", "credits": 3, "level": "Undergraduate • Year 1", "instructor": "Dr. Robert Vance", "enrolled": 38},
    {"id": "2", "code": "CS202", "title": "Data Structures & Algorithms", "department": "Computer Science", "credits": 4, "level": "Undergraduate • Year 2", "instructor": "Prof. Elena Rostova", "enrolled": 35},
    {"id": "3", "code": "SE301", "title": "Software Architecture & Design", "department": "Software Engineering", "credits": 3, "level": "Undergraduate • Year 3", "instructor": "Dr. Alan Turing", "enrolled": 30},
    {"id": "4", "code": "EE102", "title": "Digital Circuits & Logic Systems", "department": "Electrical Engineering", "credits": 4, "level": "Undergraduate • Year 1", "instructor": "Prof. Marcus Bell", "enrolled": 28},
    {"id": "5", "code": "BA201", "title": "Principles of Financial Management", "department": "Business Administration", "credits": 3, "level": "Undergraduate • Year 2", "instructor": "Dr. Sophia Reed", "enrolled": 40},
    {"id": "6", "code": "MATH201", "title": "Linear Algebra & Vector Calculus", "department": "Mathematics", "credits": 3, "level": "Undergraduate • Year 2", "instructor": "Dr. Harold Evans", "enrolled": 34},
    {"id": "7", "code": "IT305", "title": "Cloud Infrastructure & AWS Cloud", "department": "Information Technology", "credits": 3, "level": "Undergraduate • Year 3", "instructor": "Dr. Neil Armstrong", "enrolled": 39},
    {"id": "8", "code": "MED101", "title": "Human Anatomy & Physiology", "department": "Medical Science", "credits": 4, "level": "Undergraduate • Year 1", "instructor": "Dr. Gregory House", "enrolled": 32},
]

# ── Grades Database ─────────────────────────────────────────────
grades_db = [
    {"student_id": "STU-2024-001", "student_name": "Alexandra Johnson", "course_code": "CS101", "course_title": "Intro to Computer Science", "midterm": 29, "coursework": 28, "final": 39, "total": 96, "grade": "A+", "gpa": 4.0, "avatar_url": "https://ui-avatars.com/api/?name=Alexandra+Johnson&background=1e3a5f&color=fff&size=64"},
    {"student_id": "STU-2024-002", "student_name": "Marcus Williams", "course_code": "EE102", "course_title": "Digital Circuits", "midterm": 26, "coursework": 25, "final": 35, "total": 86, "grade": "B+", "gpa": 3.3, "avatar_url": "https://ui-avatars.com/api/?name=Marcus+Williams&background=2563eb&color=fff&size=64"},
    {"student_id": "STU-2024-003", "student_name": "Sophie Chen", "course_code": "BA201", "course_title": "Financial Management", "midterm": 30, "coursework": 29, "final": 38, "total": 97, "grade": "A+", "gpa": 4.0, "avatar_url": "https://ui-avatars.com/api/?name=Sophie+Chen&background=7c3aed&color=fff&size=64"},
    {"student_id": "STU-2023-004", "student_name": "James Rodriguez", "course_code": "SE301", "course_title": "Software Architecture", "midterm": 27, "coursework": 26, "final": 36, "total": 89, "grade": "A", "gpa": 3.7, "avatar_url": "https://ui-avatars.com/api/?name=James+Rodriguez&background=059669&color=fff&size=64"},
    {"student_id": "STU-2024-006", "student_name": "Daniel Kim", "course_code": "IT305", "course_title": "Cloud Infrastructure", "midterm": 28, "coursework": 27, "final": 37, "total": 92, "grade": "A", "gpa": 3.8, "avatar_url": "https://ui-avatars.com/api/?name=Daniel+Kim&background=0891b2&color=fff&size=64"},
    {"student_id": "STU-2023-005", "student_name": "Emily Thompson", "course_code": "MATH201", "course_title": "Linear Algebra", "midterm": 16, "coursework": 18, "final": 22, "total": 56, "grade": "D", "gpa": 1.5, "avatar_url": "https://ui-avatars.com/api/?name=Emily+Thompson&background=dc2626&color=fff&size=64"},
]

# ── Students Database ───────────────────────────────────────────
students_db = [
    {"id":"1","student_id":"STU-2024-001","full_name":"Alexandra Johnson","email":"a.johnson@unimanage.edu","phone":"+1-555-0101","department":"Computer Science","dob":"2002-03-15","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Alexandra+Johnson&background=1e3a5f&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"2","student_id":"STU-2024-002","full_name":"Marcus Williams","email":"m.williams@unimanage.edu","phone":"+1-555-0102","department":"Electrical Engineering","dob":"2001-07-22","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Marcus+Williams&background=2563eb&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"3","student_id":"STU-2024-003","full_name":"Sophie Chen","email":"s.chen@unimanage.edu","phone":"+1-555-0103","department":"Business Administration","dob":"2003-01-10","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Sophie+Chen&background=7c3aed&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"4","student_id":"STU-2023-004","full_name":"James Rodriguez","email":"j.rodriguez@unimanage.edu","phone":"+1-555-0104","department":"Mechanical Engineering","dob":"2001-11-30","enrollment_date":"2023-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=James+Rodriguez&background=059669&color=fff&size=128","created_at":"2023-09-01"},
    {"id":"5","student_id":"STU-2023-005","full_name":"Emily Thompson","email":"e.thompson@unimanage.edu","phone":"+1-555-0105","department":"Mathematics","dob":"2002-05-18","enrollment_date":"2023-09-01","status":"Inactive","avatar_url":"https://ui-avatars.com/api/?name=Emily+Thompson&background=dc2626&color=fff&size=128","created_at":"2023-09-01"},
    {"id":"6","student_id":"STU-2024-006","full_name":"Daniel Kim","email":"d.kim@unimanage.edu","phone":"+1-555-0106","department":"Information Technology","dob":"2003-08-25","enrollment_date":"2024-01-15","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Daniel+Kim&background=0891b2&color=fff&size=128","created_at":"2024-01-15"},
    {"id":"7","student_id":"STU-2024-007","full_name":"Isabella Martinez","email":"i.martinez@unimanage.edu","phone":"+1-555-0107","department":"Medical Science","dob":"2002-12-03","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Isabella+Martinez&background=be185d&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"8","student_id":"STU-2023-008","full_name":"Noah Anderson","email":"n.anderson@unimanage.edu","phone":"+1-555-0108","department":"Physics","dob":"2001-04-14","enrollment_date":"2023-09-01","status":"Graduated","avatar_url":"https://ui-avatars.com/api/?name=Noah+Anderson&background=92400e&color=fff&size=128","created_at":"2023-09-01"},
    {"id":"9","student_id":"STU-2024-009","full_name":"Olivia Brown","email":"o.brown@unimanage.edu","phone":"+1-555-0109","department":"Law","dob":"2002-09-07","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Olivia+Brown&background=1d4ed8&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"10","student_id":"STU-2024-010","full_name":"Liam Davis","email":"l.davis@unimanage.edu","phone":"+1-555-0110","department":"Software Engineering","dob":"2003-02-20","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Liam+Davis&background=065f46&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"11","student_id":"STU-2022-011","full_name":"Ava Wilson","email":"a.wilson@unimanage.edu","phone":"+1-555-0111","department":"Chemistry","dob":"2000-06-11","enrollment_date":"2022-09-01","status":"Graduated","avatar_url":"https://ui-avatars.com/api/?name=Ava+Wilson&background=7c2d12&color=fff&size=128","created_at":"2022-09-01"},
    {"id":"12","student_id":"STU-2024-012","full_name":"Ethan Garcia","email":"e.garcia@unimanage.edu","phone":"+1-555-0112","department":"Civil Engineering","dob":"2003-10-29","enrollment_date":"2024-01-15","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Ethan+Garcia&background=1e40af&color=fff&size=128","created_at":"2024-01-15"},
    {"id":"13","student_id":"STU-2024-013","full_name":"Mia Johnson","email":"m.johnson@unimanage.edu","phone":"+1-555-0113","department":"Biology","dob":"2003-05-17","enrollment_date":"2024-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=Mia+Johnson&background=0f766e&color=fff&size=128","created_at":"2024-09-01"},
    {"id":"14","student_id":"STU-2023-014","full_name":"William Taylor","email":"w.taylor@unimanage.edu","phone":"+1-555-0114","department":"Economics","dob":"2001-08-30","enrollment_date":"2023-09-01","status":"Active","avatar_url":"https://ui-avatars.com/api/?name=William+Taylor&background=6d28d9&color=fff&size=128","created_at":"2023-09-01"},
    {"id":"15","student_id":"STU-2022-015","full_name":"Charlotte Lee","email":"c.lee@unimanage.edu","phone":"+1-555-0115","department":"Architecture","dob":"2000-11-25","enrollment_date":"2022-09-01","status":"Suspended","avatar_url":"https://ui-avatars.com/api/?name=Charlotte+Lee&background=b45309&color=fff&size=128","created_at":"2022-09-01"},
]

def get_stats():
    total      = len(students_db)
    active     = sum(1 for s in students_db if s["status"] == "Active")
    graduated  = sum(1 for s in students_db if s["status"] == "Graduated")
    inactive   = sum(1 for s in students_db if s["status"] == "Inactive")
    suspended  = sum(1 for s in students_db if s["status"] == "Suspended")
    new_year   = sum(1 for s in students_db if s["enrollment_date"].startswith(str(date.today().year)))
    depts = {}
    for s in students_db:
        depts[s["department"]] = depts.get(s["department"], 0) + 1
    return {"total":total,"active":active,"inactive":inactive,"graduated":graduated,
            "suspended":suspended,"new_students":new_year,"total_courses":len(courses_db),"departments":depts}

# ── Authentication Routes ────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    next_url = request.args.get("next", url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Check demo users or allow valid institutional credentials
        user_data = DEMO_USERS.get(email)
        if user_data and user_data["password"] == password:
            session["user"] = {
                "name": user_data["name"],
                "role": user_data["role"],
                "email": user_data["email"],
                "avatar": user_data["avatar"]
            }
            flash(f"Welcome back, {user_data['name']}!", "success")
            return redirect(next_url or url_for("dashboard"))
        else:
            flash("Invalid email or password. Click 'Use Demo' to sign in.", "error")

    return render_template("login.html", next_url=next_url)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been signed out securely.", "success")
    return redirect(url_for("login"))

# ── Main University Routes ───────────────────────────────────────

@app.route("/")
def dashboard():
    stats  = get_stats()
    recent = sorted(students_db, key=lambda s: s["created_at"], reverse=True)[:5]
    return render_template("dashboard.html", stats=stats, recent_students=recent, departments=DEPARTMENTS)

@app.route("/students")
def students():
    q      = request.args.get("q","").strip().lower()
    dept   = request.args.get("department","")
    status = request.args.get("status","")
    page   = int(request.args.get("page",1))
    per    = app.config["STUDENTS_PER_PAGE"]
    filtered = students_db[:]
    if q:      filtered = [s for s in filtered if q in s["full_name"].lower() or q in s["email"].lower() or q in s["student_id"].lower()]
    if dept:   filtered = [s for s in filtered if s["department"] == dept]
    if status: filtered = [s for s in filtered if s["status"] == status]
    total_pages = max(1,(len(filtered)+per-1)//per)
    page        = max(1,min(page,total_pages))
    paginated   = filtered[(page-1)*per:page*per]
    return render_template("students.html", students=paginated, total_students=len(filtered),
                           current_page=page, total_pages=total_pages, departments=DEPARTMENTS,
                           q=q, dept=dept, status=status)

@app.route("/students/export")
def export_students():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Full Name", "Email", "Phone", "Department", "Date of Birth", "Enrollment Date", "Status"])
    for s in students_db:
        writer.writerow([s["student_id"], s["full_name"], s["email"], s["phone"], s["department"], s["dob"], s["enrollment_date"], s["status"]])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=unimanage_students.csv"}
    )

@app.route("/students/add", methods=["GET","POST"])
def add_student():
    if request.method == "POST":
        errors = {}
        full_name       = request.form.get("full_name","").strip()
        student_id_val  = request.form.get("student_id","").strip()
        email           = request.form.get("email","").strip()
        phone           = request.form.get("phone","").strip()
        department      = request.form.get("department","").strip()
        dob             = request.form.get("dob","").strip()
        enrollment_date = request.form.get("enrollment_date","").strip()

        if not full_name:       errors["full_name"]       = "Full name is required."
        if not student_id_val:  errors["student_id"]      = "Student ID is required."
        if not email:           errors["email"]           = "Email is required."
        elif "@" not in email:  errors["email"]           = "Enter a valid email address."
        if not phone:           errors["phone"]           = "Phone number is required."
        if not department:      errors["department"]      = "Please select a department."
        if not dob:             errors["dob"]             = "Date of birth is required."
        if not enrollment_date: errors["enrollment_date"] = "Enrollment date is required."
        for s in students_db:
            if s["student_id"] == student_id_val:  errors["student_id"] = "This Student ID already exists."
            if s["email"].lower() == email.lower(): errors["email"]      = "This email is already registered."

        avatar_url = f"https://ui-avatars.com/api/?name={full_name.replace(' ','+')}&background=1e3a5f&color=fff&size=128"
        avatar_file = request.files.get("avatar")
        if avatar_file and avatar_file.filename:
            ext = os.path.splitext(avatar_file.filename)[1].lower()
            if ext not in [".jpg",".jpeg",".png",".gif",".webp"]:
                errors["avatar"] = "Only JPG, PNG, GIF, or WebP files are allowed."
            elif not errors:
                fname = f"{uuid.uuid4().hex}{ext}"
                avatar_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
                avatar_url = url_for("static", filename=f"images/uploads/{fname}")

        if errors:
            return render_template("add_student.html", errors=errors, form=request.form, departments=DEPARTMENTS)

        students_db.insert(0,{"id":str(uuid.uuid4()),"student_id":student_id_val,"full_name":full_name,
            "email":email,"phone":phone,"department":department,"dob":dob,
            "enrollment_date":enrollment_date,"status":"Active","avatar_url":avatar_url,
            "created_at":date.today().isoformat()})
        flash(f"Student {full_name} has been registered successfully!","success")
        return redirect(url_for("students"))
    return render_template("add_student.html", errors={}, form={}, departments=DEPARTMENTS)

@app.route("/students/<student_id>/edit", methods=["GET","POST"])
def edit_student(student_id):
    student = next((s for s in students_db if s["id"]==student_id), None)
    if not student:
        flash("Student not found.","error")
        return redirect(url_for("students"))
    if request.method == "POST":
        student["full_name"]       = request.form.get("full_name",      student["full_name"]).strip()
        student["email"]           = request.form.get("email",          student["email"]).strip()
        student["phone"]           = request.form.get("phone",          student["phone"]).strip()
        student["department"]      = request.form.get("department",     student["department"]).strip()
        student["dob"]             = request.form.get("dob",            student["dob"]).strip()
        student["enrollment_date"] = request.form.get("enrollment_date",student["enrollment_date"]).strip()
        student["status"]          = request.form.get("status",         student["status"]).strip()
        flash(f"Student {student['full_name']} updated successfully!","success")
        return redirect(url_for("students"))
    return render_template("edit_student.html", student=student, departments=DEPARTMENTS,
                           statuses=["Active","Inactive","Graduated","Suspended"])

@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    global students_db
    student = next((s for s in students_db if s["id"]==student_id), None)
    if student:
        students_db = [s for s in students_db if s["id"]!=student_id]
        flash(f"Student {student['full_name']} has been deleted.","warning")
    return redirect(url_for("students"))

# ── Courses Routes ───────────────────────────────────────────────

@app.route("/courses")
def courses():
    total_enrolled = sum(c["enrolled"] for c in courses_db)
    return render_template("courses.html", courses=courses_db, total_enrolled=total_enrolled, departments=DEPARTMENTS)

@app.route("/courses/add", methods=["POST"])
def add_course():
    code = request.form.get("code", "").strip().upper()
    title = request.form.get("title", "").strip()
    department = request.form.get("department", "").strip()
    credits = int(request.form.get("credits", 3))
    instructor = request.form.get("instructor", "").strip()

    if code and title and department:
        courses_db.insert(0, {
            "id": str(uuid.uuid4()),
            "code": code,
            "title": title,
            "department": department,
            "credits": credits,
            "level": "Undergraduate",
            "instructor": instructor or "Faculty Instructor",
            "enrolled": 0
        })
        flash(f"Course {code}: {title} added successfully!", "success")
    return redirect(url_for("courses"))

# ── Schedule Route ───────────────────────────────────────────────

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

# ── Grades Route ─────────────────────────────────────────────────

@app.route("/grades")
def grades():
    return render_template("grades.html", grade_records=grades_db)

# ── Settings Route ───────────────────────────────────────────────

@app.route("/settings")
def settings():
    aws_info = {
        "host": app.config.get("DB_HOST", "unimanage-cluster.rds.amazonaws.com"),
        "database": app.config.get("DB_NAME", "unimanage"),
        "user": app.config.get("DB_USER", "admin")
    }
    return render_template("settings.html", aws_info=aws_info)

# ── API Endpoints ────────────────────────────────────────────────

@app.route("/api/stats")
def api_stats(): return jsonify(get_stats())

@app.route("/api/students")
def api_students(): return jsonify(students_db)

@app.route("/api/students/<student_id>")
def api_student(student_id):
    s = next((s for s in students_db if s["id"]==student_id), None)
    return jsonify(s) if s else (jsonify({"error":"Not found"}),404)

@app.route("/api/departments")
def api_departments(): return jsonify(DEPARTMENTS)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
