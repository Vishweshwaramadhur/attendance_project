-- Create Teachers Table
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Students Table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Attendance Table
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Insert Teacher Account
INSERT INTO teachers (name, username, password) VALUES 
('Admin Teacher', 'teacher', 'teacher123');

-- Insert 40 Students (20 Boys and 20 Girls)
INSERT INTO students (student_id, name, gender, username, password) VALUES
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
('STD040', 'Christine Bell', 'Female', 'christine.bell', 'pass2020');