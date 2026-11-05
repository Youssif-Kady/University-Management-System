-- ================================================================
-- UniManage – Database Schema (MySQL / Amazon RDS)
-- Database Name: unimanage
-- Compatibility: MySQL 8.0+ / AWS RDS MySQL
-- ================================================================

CREATE DATABASE IF NOT EXISTS `unimanage` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `unimanage`;

-- Drop existing tables if re-initializing
DROP TABLE IF EXISTS `activity_logs`;
DROP TABLE IF EXISTS `students`;
DROP TABLE IF EXISTS `departments`;

-- 1. Departments Table
CREATE TABLE `departments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `code` VARCHAR(10) NOT NULL UNIQUE,
    `faculty` VARCHAR(100) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Students Table
CREATE TABLE `students` (
    `id` VARCHAR(36) PRIMARY KEY,
    `student_id` VARCHAR(30) NOT NULL UNIQUE,
    `full_name` VARCHAR(120) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `phone` VARCHAR(25) NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `dob` DATE NOT NULL,
    `enrollment_date` DATE NOT NULL,
    `status` ENUM('Active', 'Inactive', 'Graduated', 'Suspended') NOT NULL DEFAULT 'Active',
    `avatar_url` VARCHAR(500) NULL,
    `s3_key` VARCHAR(255) NULL COMMENT 'Amazon S3 object key for uploaded profile images',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_dept` (`department`),
    INDEX `idx_status` (`status`),
    INDEX `idx_enrollment` (`enrollment_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Activity Logs Table (System audit & dashboard activity feed)
CREATE TABLE `activity_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `student_id` VARCHAR(36) NULL,
    `action` VARCHAR(255) NOT NULL,
    `category` ENUM('enrollment', 'update', 'status_change', 'deletion', 'system') NOT NULL,
    `performed_by` VARCHAR(100) DEFAULT 'Admin',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Initial Seed Data for Departments
INSERT INTO `departments` (`name`, `code`, `faculty`) VALUES
('Computer Science', 'CS', 'Faculty of Computing & IT'),
('Information Technology', 'IT', 'Faculty of Computing & IT'),
('Software Engineering', 'SE', 'Faculty of Computing & IT'),
('Electrical Engineering', 'EE', 'Faculty of Engineering'),
('Mechanical Engineering', 'ME', 'Faculty of Engineering'),
('Civil Engineering', 'CE', 'Faculty of Engineering'),
('Business Administration', 'BA', 'Faculty of Business'),
('Economics', 'ECON', 'Faculty of Business'),
('Mathematics', 'MATH', 'Faculty of Science'),
('Physics', 'PHYS', 'Faculty of Science'),
('Chemistry', 'CHEM', 'Faculty of Science'),
('Biology', 'BIO', 'Faculty of Science'),
('Medical Science', 'MED', 'Faculty of Medicine'),
('Law', 'LAW', 'Faculty of Law'),
('Architecture', 'ARCH', 'Faculty of Engineering & Design');

-- Initial Seed Data for Students
INSERT INTO `students` (`id`, `student_id`, `full_name`, `email`, `phone`, `department`, `dob`, `enrollment_date`, `status`, `avatar_url`) VALUES
('1', 'STU-2024-001', 'Alexandra Johnson', 'a.johnson@unimanage.edu', '+1-555-0101', 'Computer Science', '2002-03-15', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Alexandra+Johnson&background=1e3a5f&color=fff&size=128'),
('2', 'STU-2024-002', 'Marcus Williams', 'm.williams@unimanage.edu', '+1-555-0102', 'Electrical Engineering', '2001-07-22', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Marcus+Williams&background=2563eb&color=fff&size=128'),
('3', 'STU-2024-003', 'Sophie Chen', 's.chen@unimanage.edu', '+1-555-0103', 'Business Administration', '2003-01-10', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Sophie+Chen&background=7c3aed&color=fff&size=128'),
('4', 'STU-2023-004', 'James Rodriguez', 'j.rodriguez@unimanage.edu', '+1-555-0104', 'Mechanical Engineering', '2001-11-30', '2023-09-01', 'Active', 'https://ui-avatars.com/api/?name=James+Rodriguez&background=059669&color=fff&size=128'),
('5', 'STU-2023-005', 'Emily Thompson', 'e.thompson@unimanage.edu', '+1-555-0105', 'Mathematics', '2002-05-18', '2023-09-01', 'Inactive', 'https://ui-avatars.com/api/?name=Emily+Thompson&background=dc2626&color=fff&size=128'),
('6', 'STU-2024-006', 'Daniel Kim', 'd.kim@unimanage.edu', '+1-555-0106', 'Information Technology', '2003-08-25', '2024-01-15', 'Active', 'https://ui-avatars.com/api/?name=Daniel+Kim&background=0891b2&color=fff&size=128'),
('7', 'STU-2024-007', 'Isabella Martinez', 'i.martinez@unimanage.edu', '+1-555-0107', 'Medical Science', '2002-12-03', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Isabella+Martinez&background=be185d&color=fff&size=128'),
('8', 'STU-2023-008', 'Noah Anderson', 'n.anderson@unimanage.edu', '+1-555-0108', 'Physics', '2001-04-14', '2023-09-01', 'Graduated', 'https://ui-avatars.com/api/?name=Noah+Anderson&background=92400e&color=fff&size=128'),
('9', 'STU-2024-009', 'Olivia Brown', 'o.brown@unimanage.edu', '+1-555-0109', 'Law', '2002-09-07', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Olivia+Brown&background=1d4ed8&color=fff&size=128'),
('10', 'STU-2024-010', 'Liam Davis', 'l.davis@unimanage.edu', '+1-555-0110', 'Software Engineering', '2003-02-20', '2024-09-01', 'Active', 'https://ui-avatars.com/api/?name=Liam+Davis&background=065f46&color=fff&size=128');

