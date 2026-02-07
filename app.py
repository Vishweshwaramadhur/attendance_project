from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

DATABASE = 'attendance.db'

# Database initialization function
def init_db():
    """Initialize database if it doesn't exist"""
    # Remove existing database to ensure clean creation
    if os.path.exists(DATABASE):
        print("Database already exists.")
        return
    
    print("Creating new database...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Check if database.sql exists
        if not os.path.exists('database.sql'):
            print("ERROR: database.sql file not found!")
            # Create tables directly if SQL file is missing
            create_tables_directly(cursor)
        else:
            # Read and execute SQL file
            with open('database.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)
        
        conn.commit()
        print("Database created successfully!")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables created: {tables}")
        
    except Exception as e:
        print(f"Error creating database: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_tables_directly(cursor):
    """Create tables directly in case SQL file is not found"""
    print("Creating tables directly...")
    
    # Create Teachers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        )
    ''')
    
    # Insert Teacher
    cursor.execute('''
        INSERT INTO teachers (name, username, password) 
        VALUES ('Admin Teacher', 'teacher', 'teacher123')
    ''')
    
    # Insert Students
    students_data = [
        ('STD001', 'James Anderson', 'Male', 'james.anderson', 'pass1001'),
        ('STD002', 'Michael Brown', 'Male', 'michael.brown', 'pass1002'),
        ('STD003', 'Robert Johnson', 'Male', 'robert.johnson', 'pass1003'),
        ('STD004', 'William Davis', 'Male', 'william.davis', 'pass1004'),
        ('STD005', 'David Wilson', 'Male', 'david.wilson', 'pass1005'),
        ('STD006', 'Richard Martinez', 'Male', 'richard.martinez', 'pass1006'),
        ('STD007', 'Joseph Garcia', 'Male', 'joseph.garcia', 'pass1007'),
        ('STD008', 'Thomas Rodriguez', 'Male', 'thomas.rodriguez', 'pass1008'),
        ('STD009', 'Christopher Lee', 'Male', 'christopher.lee', 'pass1009'),
        ('STD010', 'Daniel Walker', 'Male', 'daniel.walker', 'pass1010'),
        ('STD011', 'Matthew Hall', 'Male', 'matthew.hall', 'pass1011'),
        ('STD012', 'Anthony Allen', 'Male', 'anthony.allen', 'pass1012'),
        ('STD013', 'Donald Young', 'Male', 'donald.young', 'pass1013'),
        ('STD014', 'Mark Hernandez', 'Male', 'mark.hernandez', 'pass1014'),
        ('STD015', 'Paul King', 'Male', 'paul.king', 'pass1015'),
        ('STD016', 'Steven Wright', 'Male', 'steven.wright', 'pass1016'),
        ('STD017', 'Andrew Lopez', 'Male', 'andrew.lopez', 'pass1017'),
        ('STD018', 'Kenneth Hill', 'Male', 'kenneth.hill', 'pass1018'),
        ('STD019', 'Joshua Scott', 'Male', 'joshua.scott', 'pass1019'),
        ('STD020', 'Kevin Green', 'Male', 'kevin.green', 'pass1020'),
        ('STD021', 'Emily Adams', 'Female', 'emily.adams', 'pass2001'),
        ('STD022', 'Sarah Baker', 'Female', 'sarah.baker', 'pass2002'),
        ('STD023', 'Jessica Carter', 'Female', 'jessica.carter', 'pass2003'),
        ('STD024', 'Ashley Mitchell', 'Female', 'ashley.mitchell', 'pass2004'),
        ('STD025', 'Jennifer Perez', 'Female', 'jennifer.perez', 'pass2005'),
        ('STD026', 'Amanda Roberts', 'Female', 'amanda.roberts', 'pass2006'),
        ('STD027', 'Melissa Turner', 'Female', 'melissa.turner', 'pass2007'),
        ('STD028', 'Michelle Phillips', 'Female', 'michelle.phillips', 'pass2008'),
        ('STD029', 'Stephanie Campbell', 'Female', 'stephanie.campbell', 'pass2009'),
        ('STD030', 'Rebecca Parker', 'Female', 'rebecca.parker', 'pass2010'),
        ('STD031', 'Laura Evans', 'Female', 'laura.evans', 'pass2011'),
        ('STD032', 'Kimberly Edwards', 'Female', 'kimberly.edwards', 'pass2012'),
        ('STD033', 'Amy Collins', 'Female', 'amy.collins', 'pass2013'),
        ('STD034', 'Angela Stewart', 'Female', 'angela.stewart', 'pass2014'),
        ('STD035', 'Helen Sanchez', 'Female', 'helen.sanchez', 'pass2015'),
        ('STD036', 'Rachel Morris', 'Female', 'rachel.morris', 'pass2016'),
        ('STD037', 'Nicole Rogers', 'Female', 'nicole.rogers', 'pass2017'),
        ('STD038', 'Samantha Reed', 'Female', 'samantha.reed', 'pass2018'),
        ('STD039', 'Katherine Cook', 'Female', 'katherine.cook', 'pass2019'),
        ('STD040', 'Christine Bell', 'Female', 'christine.bell', 'pass2020')
    ]
    
    cursor.executemany('''
        INSERT INTO students (student_id, name, gender, username, password) 
        VALUES (?, ?, ?, ?, ?)
    ''', students_data)

# Get database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorators
def student_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            flash('Please login as student first.', 'danger')
            return redirect(url_for('student_login'))
        # Prevent students from accessing teacher routes
        if 'teacher_id' in session:
            flash('Unauthorized access!', 'danger')
            return redirect(url_for('unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'teacher_id' not in session:
            flash('Please login as teacher first.', 'danger')
            return redirect(url_for('teacher_login'))
        # Prevent teachers from accessing student routes with student session
        if 'student_id' in session:
            flash('Unauthorized access!', 'danger')
            return redirect(url_for('unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Unauthorized Access Page
@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html'), 403

# Student Login
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE username = ? AND password = ?', 
                              (username, password)).fetchone()
        conn.close()
        
        if student:
            session['student_id'] = student['student_id']
            session['student_name'] = student['name']
            session['user_type'] = 'student'
            flash(f'Welcome {student["name"]}!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('student_login.html')

# Teacher Login
@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        teacher = conn.execute('SELECT * FROM teachers WHERE username = ? AND password = ?', 
                              (username, password)).fetchone()
        conn.close()
        
        if teacher:
            session['teacher_id'] = teacher['id']
            session['teacher_name'] = teacher['name']
            session['user_type'] = 'teacher'
            flash(f'Welcome {teacher["name"]}!', 'success')
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('teacher_login.html')

# Student Dashboard (VIEW ONLY - No Attendance Marking)
@app.route('/student/dashboard')
@student_login_required
def student_dashboard():
    student_id = session['student_id']
    conn = get_db_connection()

    # Get student info
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()

    # Get attendance records
    attendance_records = conn.execute(
        'SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC, time DESC',
        (student_id,)
    ).fetchall()

    # Calculate statistics
    total_days = len(attendance_records)
    total_present = len([r for r in attendance_records if r['status'] == 'Present'])
    total_absent = total_days - total_present
    percentage = (total_present / total_days * 100) if total_days > 0 else 0

    conn.close()

    return render_template('student_dashboard.html',
                         student=student,
                         attendance_records=attendance_records,
                         total_days=total_days,
                         total_present=total_present,
                         total_absent=total_absent,
                         percentage=round(percentage, 2))

# DISABLED: Students cannot mark their own attendance
# Only teachers can mark attendance for students
@app.route('/student/mark_attendance', methods=['POST'])
def mark_attendance():
    # Return unauthorized - students cannot mark attendance
    return jsonify({
        'success': False,
        'message': 'Unauthorized! Only teachers can mark attendance.'
    }), 403

# Teacher Dashboard
@app.route('/teacher/dashboard')
@teacher_login_required
def teacher_dashboard():
    conn = get_db_connection()
    
    # Get statistics
    total_students = conn.execute('SELECT COUNT(*) as count FROM students').fetchone()['count']
    total_boys = conn.execute('SELECT COUNT(*) as count FROM students WHERE gender = "Male"').fetchone()['count']
    total_girls = conn.execute('SELECT COUNT(*) as count FROM students WHERE gender = "Female"').fetchone()['count']
    
    # Get today's attendance
    today = datetime.now().strftime('%Y-%m-%d')
    todays_attendance = conn.execute(
        'SELECT COUNT(*) as count FROM attendance WHERE date = ?',
        (today,)
    ).fetchone()['count']
    
    conn.close()
    
    return render_template('teacher_dashboard.html',
                         total_students=total_students,
                         total_boys=total_boys,
                         total_girls=total_girls,
                         todays_attendance=todays_attendance)

# Teacher - View Students List
@app.route('/teacher/students')
@teacher_login_required
def teacher_students_list():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY student_id').fetchall()
    conn.close()
    
    return render_template('teacher_students_list.html', students=students)

# Teacher - View Student Attendance
@app.route('/teacher/student/<student_id>/attendance')
@teacher_login_required
def teacher_view_attendance(student_id):
    filter_date = request.args.get('date', '')
    
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('teacher_students_list'))
    
    # Get attendance records
    if filter_date:
        attendance_records = conn.execute(
            'SELECT * FROM attendance WHERE student_id = ? AND date = ? ORDER BY date DESC, time DESC',
            (student_id, filter_date)
        ).fetchall()
    else:
        attendance_records = conn.execute(
            'SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC, time DESC',
            (student_id,)
        ).fetchall()
    
    # Calculate statistics
    total_days = len(conn.execute('SELECT * FROM attendance WHERE student_id = ?', (student_id,)).fetchall())
    total_present = len(conn.execute('SELECT * FROM attendance WHERE student_id = ? AND status = "Present"', (student_id,)).fetchall())
    percentage = (total_present / total_days * 100) if total_days > 0 else 0
    
    conn.close()
    
    return render_template('teacher_view_attendance.html',
                         student=student,
                         attendance_records=attendance_records,
                         total_days=total_days,
                         total_present=total_present,
                         percentage=round(percentage, 2),
                         filter_date=filter_date)

# Teacher - Mark Attendance for Student (Present/Absent)
@app.route('/teacher/mark_attendance/<student_id>', methods=['POST'])
@teacher_login_required
def teacher_mark_attendance(student_id):
    today = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')

    # Get status from form (default: Present)
    status = request.form.get('status', 'Present')

    conn = get_db_connection()

    # Check if already marked today
    existing = conn.execute(
        'SELECT * FROM attendance WHERE student_id = ? AND date = ?',
        (student_id, today)
    ).fetchone()

    if existing:
        conn.close()
        flash('Attendance already marked for this student today!', 'warning')
        return redirect(url_for('teacher_students_list'))

    # Insert attendance
    conn.execute(
        'INSERT INTO attendance (student_id, date, time, status) VALUES (?, ?, ?, ?)',
        (student_id, today, current_time, status)
    )
    conn.commit()

    # Get student name
    student = conn.execute('SELECT name FROM students WHERE student_id = ?', (student_id,)).fetchone()
    conn.close()

    flash(f'Attendance marked as {status} for {student["name"]}!', 'success')
    return redirect(url_for('teacher_students_list'))

# Teacher - Bulk Attendance Marking Page
@app.route('/teacher/mark_attendance_bulk', methods=['GET', 'POST'])
@teacher_login_required
def mark_attendance_bulk():
    conn = get_db_connection()

    if request.method == 'POST':
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')

        # Get all student IDs and their attendance status
        marked_count = 0
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                student_id = key.replace('attendance_', '')

                # Check if already marked today
                existing = conn.execute(
                    'SELECT * FROM attendance WHERE student_id = ? AND date = ?',
                    (student_id, today)
                ).fetchone()

                if not existing:
                    # Insert attendance
                    conn.execute(
                        'INSERT INTO attendance (student_id, date, time, status) VALUES (?, ?, ?, ?)',
                        (student_id, today, current_time, value)
                    )
                    marked_count += 1

        conn.commit()
        conn.close()

        if marked_count > 0:
            flash(f'Attendance marked successfully for {marked_count} student(s)!', 'success')
        else:
            flash('Attendance already marked for all selected students today!', 'warning')

        return redirect(url_for('mark_attendance_bulk'))

    # GET request - show form
    today = datetime.now().strftime('%Y-%m-%d')

    # Get all students
    students = conn.execute('SELECT * FROM students ORDER BY student_id').fetchall()

    # Check which students already have attendance today
    marked_today = {}
    for student in students:
        record = conn.execute(
            'SELECT status FROM attendance WHERE student_id = ? AND date = ?',
            (student['student_id'], today)
        ).fetchone()
        marked_today[student['student_id']] = record['status'] if record else None

    conn.close()

    return render_template('teacher_mark_attendance_bulk.html',
                         students=students,
                         marked_today=marked_today,
                         today=today)

# Teacher - Delete Student
@app.route('/teacher/delete_student/<student_id>', methods=['POST'])
@teacher_login_required
def delete_student(student_id):
    conn = get_db_connection()

    # Delete attendance records first
    conn.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))

    # Delete student
    conn.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

    flash('Student deleted successfully!', 'success')
    return redirect(url_for('teacher_students_list'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)