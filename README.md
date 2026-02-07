# Attendance Management System

A complete web-based Attendance Management System built with Flask, SQLite, Bootstrap 5, and JavaScript. **Teacher-controlled attendance marking system** where only teachers can mark student attendance.

## Features

### Student Features (View-Only)
- Secure login system
- **View-only dashboard** (cannot mark own attendance)
- View personal attendance history (Present/Absent records)
- View attendance statistics (total days, present days, absent days, percentage)
- Real-time statistics display

### Teacher Features (Full Control)
- Secure login system
- **Bulk attendance marking** - Mark all students at once
- **Individual attendance marking** - Mark students one by one (Present/Absent)
- View dashboard with statistics
- View all students list
- View any student's attendance history
- Filter attendance by date
- Delete students
- View total students, boys, girls count
- Today's attendance summary

## Technology Stack
- **Backend**: Python Flask 3.0.0
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Authentication**: Flask Sessions
- **Security**: Role-based access control, unauthorized access prevention

## Installation & Setup

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vishweshwaramadhur/attendance_project.git
cd attendance_project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
```

### Step 4: Run the Application
```bash
python app.py
```

The application will:
1. Automatically check if `attendance.db` exists
2. If not, create the database using `database.sql`
3. Start the Flask development server on `http://0.0.0.0:5000`

### Step 5: Access the Application
Open your web browser and go to:
```
http://127.0.0.1:5000/
```

Or from another device on the same network:
```
http://YOUR_IP_ADDRESS:5000/
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
├── app.py                              # Main Flask application
├── database.sql                        # SQL schema and seed data
├── attendance.db                       # SQLite database (auto-created)
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
├── templates/
│   ├── base.html                      # Base template with navigation
│   ├── home.html                      # Landing page
│   ├── student_login.html             # Student login page
│   ├── teacher_login.html             # Teacher login page
│   ├── student_dashboard.html         # Student dashboard (VIEW ONLY)
│   ├── teacher_dashboard.html         # Teacher dashboard
│   ├── teacher_students_list.html     # Students list for teacher
│   ├── teacher_view_attendance.html   # View student attendance
│   ├── teacher_mark_attendance_bulk.html  # Bulk attendance marking (NEW)
│   └── unauthorized.html              # 403 Unauthorized access page (NEW)
└── static/
    ├── style.css                      # Custom CSS styles
    └── main.js                        # JavaScript for frontend
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
- status (Present/Absent)
- created_at

## How Database is Created

The `init_db()` function in `app.py`:
1. Checks if `attendance.db` file exists
2. If not found, reads `database.sql`
3. Executes all SQL commands to create tables
4. Inserts seed data (1 teacher + 40 students)
5. Database is ready to use!

## Key Features Implementation

### Teacher-Controlled Attendance
- **Bulk Marking**: Mark all students' attendance at once with Present/Absent options
- **Individual Marking**: Quick buttons to mark individual students
- **No Student Marking**: Students cannot mark their own attendance (security enforced)

### Security Features
- Session-based authentication
- Login required decorators
- Role-based access control (students cannot access teacher pages)
- Unauthorized access returns 403 error page
- Student attendance marking route disabled (returns 403 Forbidden)

### Validation
- Teachers cannot mark duplicate attendance for same day
- Attendance status: Present or Absent
- Date-based filtering for reports

## Usage Guide

### For Students:
1. Login with your username and password
2. **View your attendance dashboard** (read-only)
3. Check your attendance history
4. View your attendance statistics
5. Logout when done

**Note**: Students cannot mark their own attendance. Only teachers can mark attendance.

### For Teachers:

#### Bulk Attendance Marking:
1. Login with teacher credentials
2. Click **"Mark Attendance"** button on dashboard
3. Select Present (✓) or Absent (✗) for each student
4. Click **"Submit Attendance"** button
5. Only selected students will be marked

#### Individual Attendance Marking:
1. Go to **"View All Students"**
2. For each student, click:
   - Green ✓ button → Mark Present
   - Yellow ✗ button → Mark Absent
3. Confirmation message appears

#### View Reports:
1. Click **"View All Students"**
2. Click on any student to view their attendance history
3. Use date filter to view specific dates
4. View statistics and attendance percentage

#### Other Actions:
- **Delete students**: Click red trash icon (with confirmation)
- **View dashboard statistics**: See total students, boys, girls, today's attendance

## Security Notes

### Important for Production:
1. **Change the secret key** in `app.py`:
   ```python
   app.secret_key = 'your_secret_key_here_change_in_production'
   ```
   Generate a secure random key:
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Disable debug mode** in production:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

4. **Change default passwords** for all accounts

## Troubleshooting

### Database Not Created
- Make sure `database.sql` file is in the same directory as `app.py`
- Check file permissions

### Module Not Found Error
- Run `pip install -r requirements.txt` again
- Make sure you're using the correct Python environment
- Activate virtual environment if using one

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000:
  ```bash
  # Linux/Mac
  lsof -ti:5000 | xargs kill -9

  # Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Cannot Access from Other Devices
- Make sure `host='0.0.0.0'` in `app.run()`
- Check firewall settings
- Verify you're using the correct IP address

## Recent Updates

### Version 2.0 (Latest)
- ✅ **Removed student attendance marking capability**
- ✅ Student dashboard is now **view-only**
- ✅ Added **bulk attendance marking** for teachers
- ✅ Added **Present/Absent** status support
- ✅ Enhanced security with 403 unauthorized page
- ✅ Improved UI with better button grouping
- ✅ Added absent days statistics
- ✅ Updated teacher dashboard with quick actions

### Version 1.0
- Initial release with student self-marking

## Contributing
This is an educational project. Feel free to fork and modify as needed.

## License
This project is for educational purposes.

## Support
For issues or questions:
- Check the troubleshooting section
- Verify all files are in correct locations
- Ensure Python and pip are properly installed
- Check that no firewall is blocking the port

---
**Developed with Flask & Bootstrap**
**Repository**: https://github.com/vishweshwaramadhur/attendance_project
