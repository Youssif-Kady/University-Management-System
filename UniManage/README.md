# UniManage – University Student Management System

A modern, responsive, commercial-grade Student Management System designed with a SaaS dashboard UI, deep navy aesthetics, fluid animations, and production AWS cloud architecture.

---

## 🌟 Key Features

### 1. Dashboard (`/`)
- **KPI Metrics:** Total Students, Active Students, New Students (current year), and Total Courses with animated counters.
- **Interactive Analytics:**
  - Student Enrollment Trend (Monthly vs. Yearly toggle) with Chart.js line gradients.
  - Distribution by Department with dynamic doughnut charts.
  - Real-time Status Breakdown (Active, Inactive, Graduated, Suspended).
- **Recent Activity Feed & Recent Students Table:** Instant overview of new additions and status changes.
- **Quick Action Bar:** Fast-track shortcuts to key tasks.

### 2. Students Directory (`/students`)
- **Data Table:** Modern data view with student avatars, ID badges, department tags, and status pills.
- **Search & Filtering:**
  - Real-time search by name, student ID, and email with keyword highlighting.
  - Dropdown filter by department and status.
  - Interactive department tags (click any department badge in table to filter).
- **Sorting & Multi-select:** Interactive client-side column sorting and "select-all" checkboxes.
- **Pagination:** Clean, numbered pagination with previous/next controls.
- **Delete Confirmation Modal:** Protects against accidental removals with a safety modal.

### 3. Student Registration & Profile (`/students/add`, `/students/<id>/edit`)
- **Registration Form:** Complete fields for Name, Student ID, Email, Phone, Department, Date of Birth, and Enrollment Date.
- **Interactive ID Card Preview:** Dynamic ID badge updates live as you type name, ID, and select department.
- **Avatar Uploader:** Live image preview with 5MB validation.
- **Dual Validation:** Client-side real-time checks + server-side validation with clean feedback.

---

## 🏗️ Project Structure

```
UniManage/
├── app.py                  # Flask Application & Route Controllers
├── config.py               # Environment & App Configuration
├── aws_service.py          # AWS Integration points (S3, RDS, EC2/VPC)
├── requirements.txt        # Python Dependencies
├── schema.sql              # MySQL Database Schema for Amazon RDS
├── Dockerfile              # Docker container definition for AWS EC2/ECS
├── .env.example            # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css       # Custom SaaS Theme & Responsive Layout
│   └── js/
│       ├── main.js         # Core UI: Sidebar, Modals, Counters, Toasts
│       ├── dashboard.js    # Chart.js visualisations & toggle logic
│       ├── students.js     # Search, filter, sorting, and row click
│       └── add_student.js  # Live card preview, avatar upload, validation
└── templates/
    ├── base.html           # Master layout with sidebar & topbar
    ├── dashboard.html      # Page 1: Dashboard
    ├── students.html       # Page 2: Student Management
    ├── add_student.html    # Page 3: Add New Student
    └── edit_student.html   # Edit Student Profile
```

---

## 🚀 Getting Started Locally

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Install Dependencies
```bash
cd UniManage
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## ☁️ AWS Cloud Deployment Architecture

The application has been prepared with clean integration points for AWS:

```
[ Internet ]
     │
     ▼
[ Application Load Balancer / Amazon VPC Public Subnet ]
     │
     ▼
[ Amazon EC2 (Gunicorn / Docker) ]  ───►  [ Amazon S3 ] (Student Avatars)
     │
     ▼ (Private Subnet)
[ Amazon RDS (MySQL 8.0 Multi-AZ) ]
```

### 1. Amazon EC2
- Runs the application behind **Gunicorn** or inside Docker.
- Configured via environment variables (`.env`).
- Deploy with `docker build -t unimanage . && docker run -p 5000:5000 unimanage`.

### 2. Amazon RDS (MySQL)
- Execute `schema.sql` on your RDS instance to create tables and indexes.
- Update `DB_HOST`, `DB_USER`, `DB_PASSWORD` in `.env`.

### 3. Amazon S3
- Bucket configured in `aws_service.py` (`S3StorageService`).
- Handles student avatar upload with pre-signed URL capabilities.

### 4. Amazon VPC
- Place EC2 instances in private subnets with an Internet Gateway + NAT Gateway.
- RDS database in isolated database subnets accessible only from EC2 security group on port 3306.

