DROP DATABASE IF EXISTS placement_db;
CREATE DATABASE placement_db;
USE placement_db;

CREATE TABLE ROLES (
    rol_id INT AUTO_INCREMENT PRIMARY KEY,
    rol_desc VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE PERMISSION (
    per_id INT AUTO_INCREMENT PRIMARY KEY,
    per_name VARCHAR(100) NOT NULL,
    per_module VARCHAR(100),
    per_desc VARCHAR(255)
);

CREATE TABLE ROLE_PERMISSION (
    rol_id INT NOT NULL,
    per_id INT NOT NULL,
    PRIMARY KEY (rol_id, per_id),
    FOREIGN KEY (rol_id) REFERENCES ROLES(rol_id) ON DELETE CASCADE,
    FOREIGN KEY (per_id) REFERENCES PERMISSION(per_id) ON DELETE CASCADE
);

CREATE TABLE USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(100),
    user_address VARCHAR(255),
    rol_id INT NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES ROLES(rol_id) ON DELETE RESTRICT
);

CREATE TABLE LOGIN (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    login_username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
);

CREATE TABLE USER_PHONE (
    phone_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
);

CREATE TABLE STUDENT (
    stu_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    stu_name VARCHAR(100) NOT NULL,
    stu_email VARCHAR(100),
    stu_phone VARCHAR(20),
    stu_dept VARCHAR(100),
    stu_cgpa DECIMAL(4, 2),
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
);

CREATE TABLE COMPANY (
    com_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    com_name VARCHAR(255) NOT NULL,
    com_desc TEXT,
    com_type VARCHAR(100),
    com_add VARCHAR(255),
    salary_min VARCHAR(50),
    salary_max VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE
);

CREATE TABLE JOB (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    com_id INT NOT NULL,
    job_name VARCHAR(100) NOT NULL,
    job_vacancy INT NOT NULL CHECK (job_vacancy > 0),
    job_type VARCHAR(100),
    salary_min VARCHAR(50),
    salary_max VARCHAR(50),
    FOREIGN KEY (com_id) REFERENCES COMPANY(com_id) ON DELETE CASCADE
);

CREATE TABLE COLLEGE (
    col_id INT AUTO_INCREMENT PRIMARY KEY,
    col_desc VARCHAR(255) NOT NULL,
    col_add VARCHAR(255)
);

CREATE TABLE PLACEMENTS (
    plcm_id INT AUTO_INCREMENT PRIMARY KEY,
    stu_id INT NOT NULL,
    job_id INT NOT NULL,
    plcm_desc TEXT,
    status ENUM('Applied', 'Selected', 'Rejected') DEFAULT 'Applied',
    UNIQUE KEY unique_application (stu_id, job_id),
    FOREIGN KEY (stu_id) REFERENCES STUDENT(stu_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
);

-- Initial Data Setup
INSERT INTO ROLES (rol_id, rol_desc) VALUES (1, 'Admin');
INSERT INTO ROLES (rol_id, rol_desc) VALUES (2, 'Student');
INSERT INTO ROLES (rol_id, rol_desc) VALUES (3, 'Company');
