CREATE DATABASE IF NOT EXISTS hospital_db;

USE hospital_db;

CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO staff
(name, role, department, email, phone)
VALUES
(
    'Dr. Rahul Sharma',
    'Doctor',
    'Cardiology',
    'rahul@example.com',
    '9876543210'
),
(
    'Priya Patil',
    'Nurse',
    'Emergency',
    'priya@example.com',
    '9876543211'
);
