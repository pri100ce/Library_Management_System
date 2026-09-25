-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 04, 2026 at 04:35 AM
-- Server version: 8.0.45
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library_db`
--
CREATE DATABASE IF NOT EXISTS `library_db`;
USE `library_db`;
-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int NOT NULL,
  `activity` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `activity`, `created_at`) VALUES
(1, '📚 New book added : Rich Dad Poor Dad', '2026-07-03 15:55:49'),
(2, '👨 Student registered : Haresh Patadiya', '2026-07-03 15:57:23'),
(3, '📤 A book was issued.', '2026-07-03 15:58:04'),
(4, '📥 A book was returned.', '2026-07-03 17:11:47'),
(5, '📤 A book was issued.', '2026-07-04 06:50:46'),
(6, '📥 A book was returned.', '2026-07-17 15:44:56'),
(7, '📤 A book was issued.', '2026-07-17 16:50:03'),
(8, '📥 A book was returned.', '2026-07-17 16:50:36'),
(9, '📚 New book added : Prince of Persia', '2026-07-18 11:55:40'),
(10, '👨 Student registered : Hitesh Bhatiya', '2026-07-18 11:57:25'),
(11, '📤 A book was issued.', '2026-07-18 11:59:00'),
(12, '📥 A book was returned.', '2026-07-18 12:00:08'),
(13, '📤 A book was issued.', '2026-07-18 12:46:52'),
(14, '📤 A book was issued.', '2026-07-18 12:48:13'),
(15, '📥 A book was returned.', '2026-07-18 13:10:17'),
(16, '📤 A book was issued.', '2026-07-18 13:37:26'),
(17, '📥 A book was returned.', '2026-08-02 10:45:54'),
(18, '📚 New book added : That One Day', '2026-08-02 11:10:39'),
(19, '📚 New book added : The Jungle Book', '2026-08-02 11:14:52'),
(20, '📚 New book added : Little Krishna', '2026-08-02 11:22:01'),
(21, '📚 New book added : Do Different : The Untold Dhoni', '2026-08-02 11:27:01'),
(22, '📚 New book added : Partner In Crime', '2026-08-02 11:30:41'),
(23, '📚 New book added : You Cant Beat Me', '2026-08-02 11:35:31'),
(24, '📚 New book added : The Lost City Dwarka', '2026-08-02 11:39:56'),
(25, '📤 A book was issued.', '2026-08-02 13:17:22'),
(26, '📤 A book was issued.', '2026-08-02 13:42:29');

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `theme` varchar(10) NOT NULL DEFAULT 'light',
  `profile_image` varchar(255) DEFAULT NULL
);

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `name`, `username`, `email`, `password`, `theme`, `profile_image`) VALUES
(1, 'Prince', 'admin', 'admin@gmail.com', 'ima@2105', 'light', 'admin.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int NOT NULL,
  `book_name` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `cover_image` varchar(255) DEFAULT NULL
);

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `book_name`, `author`, `category`, `quantity`, `cover_image`) VALUES
(1, 'The Prince', 'James Will', 'History', 5, '1.jpg'),
(2, 'One Night', 'Babu Rao', 'Thriller', 1, '2.jpg'),
(3, 'Rich Dad Poor Dad', 'Mark Benz', 'Finance', 2, '3.jpg'),
(4, 'Prince of Persia', 'Anthony', 'History', 2, '4.jpg'),
(5, 'That One Day', 'Kalidas', 'Philosophy', 2, '5.jpg'),
(6, 'The Jungle Book', 'Rudyard Kipling', 'Fiction', 2, '6.jpg'),
(7, 'Little Krishna', 'Komal Raikwar', 'Mythology', 2, '7.jpg'),
(8, 'Do Different : The Untold Dhoni', 'Amit Sinha', 'Sports', 1, '8.webp'),
(9, 'Partner In Crime', 'Jony D', 'Comedy', 2, '9.jpg'),
(10, 'You Cant Beat Me', 'Jay Singh', 'Psychological', 2, '10.jpg'),
(11, 'The Lost City Dwarka', 'S.R Rao', 'Mythology', 2, '11.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `issued_books`
--

CREATE TABLE `issued_books` (
  `id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `book_id` int DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Issued',
  `fine_amount` decimal(10,2) DEFAULT '0.00',
  `fine_status` enum('Pending','Paid') DEFAULT 'Paid'
);

--
-- Dumping data for table `issued_books`
--

INSERT INTO `issued_books` (`id`, `student_id`, `book_id`, `issue_date`, `return_date`, `status`, `fine_amount`, `fine_status`) VALUES
(7, 1, 2, '2026-07-01', '2026-07-01', 'Returned', 10.00, 'Paid'),
(8, 2, 2, '2026-06-28', '2026-06-30', 'Returned', 15.00, 'Paid'),
(9, 3, 3, '2026-07-03', '2026-07-04', 'Returned', 0.00, 'Paid'),
(10, 1, 1, '2026-07-04', '2026-07-10', 'Returned', 35.00, 'Paid'),
(11, 1, 2, '2026-07-17', '2026-08-01', 'Returned', 0.00, 'Paid'),
(12, 4, 4, '2026-07-18', '2026-08-02', 'Returned', 0.00, 'Paid'),
(14, 1, 4, '2026-07-18', '2026-08-02', 'Returned', 0.00, 'Paid'),
(15, 1, 4, '2026-07-18', '2026-08-02', 'Returned', 0.00, 'Paid'),
(16, 3, 8, '2026-08-02', '2026-08-17', 'Issued', 0.00, 'Paid'),
(17, 1, 2, '2026-08-02', '2026-08-17', 'Issued', 0.00, 'Paid');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `class` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL DEFAULT 'student123',
  `theme` varchar(10) NOT NULL DEFAULT 'light',
  `profile_image` varchar(255) DEFAULT NULL
);

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `class`, `phone`, `email`, `password`, `theme`, `profile_image`) VALUES
(1, 'Surela Prince', '12', '1457856895', 'prince@gmail.com', 'ima@2105', 'light', '1.png'),
(2, 'Mehul Sakariya', '12', '2356898589', NULL, 'student123', 'light', NULL),
(3, 'Haresh Patadiya', '12', '5485956565', NULL, 'student123', 'light', NULL),
(4, 'Hitesh Bhatiya', '12', '1235464789', NULL, 'student123', 'light', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `issued_books`
--
ALTER TABLE `issued_books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `issued_books`
--
ALTER TABLE `issued_books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `issued_books`
--
ALTER TABLE `issued_books`
  ADD CONSTRAINT `issued_books_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `issued_books_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
