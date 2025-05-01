-- Use the correct database
USE studentdbms;

-- --------------------------------------------------------
-- Table: User (for authentication)
CREATE TABLE IF NOT EXISTS `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50),
  `email` VARCHAR(50) UNIQUE,
  `password` VARCHAR(1000),  -- Store hashed password
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: Item (Inventory)
CREATE TABLE IF NOT EXISTS `item` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100),
  `category` VARCHAR(100),
  `quantity` INT,
  `price` FLOAT,
  `date_added` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: Sale (for Sales Tracking)
CREATE TABLE IF NOT EXISTS `sale` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT,
  `quantity` INT,
  `sale_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`item_id`) REFERENCES `item`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: Student (for Student Information)
CREATE TABLE IF NOT EXISTS `student` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rollno` VARCHAR(20) UNIQUE,
  `sname` VARCHAR(100),
  `sem` INT,
  `gender` VARCHAR(10),
  `branch` VARCHAR(100),
  `email` VARCHAR(100),
  `phone` VARCHAR(15),
  `address` VARCHAR(200),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: Attendance (for tracking student attendance)
CREATE TABLE IF NOT EXISTS `attendance` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT,
  `date` DATE,
  `status` VARCHAR(20),  -- 'Present' or 'Absent'
  PRIMARY KEY (`id`),
  FOREIGN KEY (`student_id`) REFERENCES `student`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------
-- Table: Grade (for storing student grades)
CREATE TABLE IF NOT EXISTS `grade` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT,
  `subject` VARCHAR(100),
  `grade` VARCHAR(2),  -- Example: 'A', 'B+', etc.
  PRIMARY KEY (`id`),
  FOREIGN KEY (`student_id`) REFERENCES `student`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
