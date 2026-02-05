# Attendance Management System

A complete web-based Attendance Management System built with Flask, SQLite, Bootstrap 5, and JavaScript (Fetch API).

## Features

### Student Features
- Secure login system
- Mark attendance (once per day)
- View personal attendance history
- View attendance statistics (total days, present days, percentage)
- Real-time attendance marking without page reload (AJAX)

### Teacher Features
- Secure login system
- View dashboard with statistics
- View all students list
- View any student's attendance history
- Filter attendance by date
- Mark attendance for students
- Delete students
- View total students, boys, girls count

## Technology Stack
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript (Fetch API)
- **Authentication**: Flask Sessions

## Installation & Setup

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)

### Step 1: Extract the Project
Extract all files to a folder named `attendance_project`

### Step 2: Install Required Packages
Open terminal/command prompt in the project directory and run:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
```

### Step 3: Run the Application
```bash
python app.py
```

The application will:
1. Automatically check if `attendance.db` exists
2. If not, create the database using `database.sql`
3. Start the Flask development server

### Step 4: Access the Application
Open your web browser and go to:
```
http://127.0.0.1:5000/
```

## Default Login Credentials

### Teacher Login
- **Username**: `teacher`
- **Password**: `teacher123`

### Student Login Examples
Students cannot self-register. Here are some example student accounts:

| Student ID | Username       | Password | Gender |
| ---------- | -------------- | -------- | ------ |
| STD001     | james.anderson | pass1001 | Male   |
| STD002     | michael.brown  | pass1002 | Male   |
| STD021     | emily.adams    | pass2001 | Female |
| STD022     | sarah.baker    | pass2002 | Female |

(Total 40 students from STD001 to STD040 are pre-loaded)

## Project Structure
```
attendance_project/
├── app.py                          # Main Flask application
├── database.sql                    # SQL schema and seed data
├── attendance.db                   # SQLite database (auto-created)
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── templates/
│   ├── base.html                  # Base template
│   ├── home.html                  # Landing page
│   ├── student_login.html         # Student login page
│   ├── teacher_login.html         # Teacher login page
│   ├── student_dashboard.html     # Student dashboard
│   ├── teacher_dashboard.html     # Teacher dashboard
│   ├── teacher_students_list.html # Students list for teacher
│   └── teacher_view_attendance.html # View student attendance
├── static/
│   ├── style.css                  # Custom CSS styles
│   └── main.js                    # JavaScript for AJAX functionality
```

## Database Schema

### Teachers Table
- id (PRIMARY KEY)
- name
- username (UNIQUE)
- password
- created_at

### Students Table
- id (PRIMARY KEY)
- student_id (UNIQUE)
- name
- gender
- username (UNIQUE)
- password
- created_at

### Attendance Table
- id (PRIMARY KEY)
- student_id (FOREIGN KEY)
- date
- time
- status
- created_at

## How Database is Created

The `init_db()` function in `app.py`:
1. Checks if `attendance.db` file exists
2. If not found, reads `database.sql`
3. Executes all SQL commands to create tables
4. Inserts seed data (1 teacher + 40 students)
5. Database is ready to use!

## Key Features Implementation

### AJAX Attendance Marking
- Uses JavaScript Fetch API
- No page reload required
- Real-time success/error messages
- Automatic statistics update

### Security
- Session-based authentication
- Login required decorators
- Role-based access control
- Students cannot access teacher pages
- Teachers cannot access student dashboards

### Validation
- Students can mark attendance only once per day
- Duplicate attendance prevention
- Date-based filtering

## Usage Guide

### For Students:
1. Login with your username and password
2. Click "Mark Attendance" button
3. View your attendance history
4. Check your attendance statistics
5. Logout when done

### For Teachers:
1. Login with teacher credentials
2. View dashboard statistics
3. Click "View Students" to see all students
4. Click on any student to view their attendance
5. Use date filter to view specific date attendance
6. Mark attendance for absent students (optional)
7. Delete students if needed (optional)
8. Logout when done

## Troubleshooting

### Database Not Created
- Make sure `database.sql` file is in the same directory as `app.py`
- Check file permissions

### Module Not Found Error
- Run `pip install -r requirements.txt` again
- Make sure you're using the correct Python environment

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

## Support
For issues or questions, check:
- All files are in correct locations
- Python and pip are properly installed
- No firewall blocking port 5000

## License
This project is for educational purposes.

---
**Developed with Flask & Bootstrap**