DROP TABLE IF EXISTS students;
CREATE TABLE students(
    student_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    dob TEXT,
    amount_due REAL
);