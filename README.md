# Attendance Management System

A web-based attendance management system where teachers can mark and track student attendance.

## Tech Stack

- **Backend:** Flask, SQLite
- **Frontend:** Bootstrap 5, JavaScript

## Setup

```bash
git clone https://github.com/vishweshwaramadhur/attendance_project.git
cd attendance_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

The database is auto-created on first run using `database.sql`.

## Default Credentials

| Role    | Username | Password   |
| ------- | -------- | ---------- |
| Teacher | teacher  | teacher123 |

40 student accounts are pre-loaded (STD001–STD040). Example: `james.anderson` / `pass1001`.

## Features

**Teacher** — Mark attendance (bulk or individual), view/filter reports, manage students

**Student** — View own attendance history and statistics (read-only)

## Project Structure

```
├── app.py              # Flask application
├── database.sql        # Schema and seed data
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
└── static/             # CSS and JS
```

## License

This project is for educational purposes.
