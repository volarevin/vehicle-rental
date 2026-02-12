-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 12, 2026 at 07:04 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vehicle_rental`
--

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `reservation_id` int NOT NULL,
  `user_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('Pending','Active','Completed','Cancelled','Rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Pending',
  `insurance_added` tinyint(1) DEFAULT '0',
  `total_cost` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cancel_reason` text COLLATE utf8mb4_general_ci,
  `reject_reason` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`reservation_id`, `user_id`, `vehicle_id`, `start_date`, `end_date`, `status`, `insurance_added`, `total_cost`, `created_at`, `cancel_reason`, `reject_reason`) VALUES
(1, 4, 1, '2026-01-20', '2026-01-22', 'Completed', 0, 3000.00, '2026-01-20 00:54:26', NULL, NULL),
(2, 4, 1, '2026-01-20', '2026-01-22', 'Cancelled', 0, 3000.00, '2026-01-20 00:59:03', NULL, NULL),
(3, 4, 5, '2026-01-22', '2026-01-29', 'Completed', 1, 12250.00, '2026-01-22 02:07:38', NULL, NULL),
(4, 4, 2, '2026-01-22', '2026-01-26', 'Completed', 0, 10000.00, '2026-01-22 02:24:50', NULL, NULL),
(5, 13, 5, '2026-02-12', '2026-02-17', 'Completed', 1, 5000.00, '2026-02-12 14:07:47', NULL, NULL),
(6, 4, 1, '2026-02-13', '2026-02-14', 'Cancelled', 0, 1500.00, '2026-02-12 18:01:18', 'maintenance', NULL),
(7, 13, 2, '2026-02-13', '2026-02-17', 'Cancelled', 1, 12000.00, '2026-02-12 18:28:02', 'change of mind', NULL),
(8, 13, 2, '2026-02-13', '2026-02-15', 'Rejected', 1, 6000.00, '2026-02-12 18:46:04', NULL, 'maintenance sorry');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `role` enum('Admin','Receptionist','Member') COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `first_name`, `last_name`, `role`, `created_at`) VALUES
(1, 'admin', '$2b$12$aJxe.G6esIjlTvME69EXKO8Wub7Mvmk/vUOeMrfbGZbY7B5EpsWHS', 'System', 'Admin', 'Admin', '2026-01-20 00:45:12'),
(2, 'sherwin', '$2b$12$aJxe.G6esIjlTvME69EXKO8Wub7Mvmk/vUOeMrfbGZbY7B5EpsWHS', 'Sherwin', 'Arizobal', 'Receptionist', '2026-01-20 00:45:12'),
(3, 'james', '$2b$12$aJxe.G6esIjlTvME69EXKO8Wub7Mvmk/vUOeMrfbGZbY7B5EpsWHS', 'James', 'Banaag', 'Receptionist', '2026-01-20 00:45:12'),
(4, 'bien', '$2b$12$aJxe.G6esIjlTvME69EXKO8Wub7Mvmk/vUOeMrfbGZbY7B5EpsWHS', 'Bien', 'Hipolito', 'Member', '2026-01-20 00:45:12'),
(13, 'pogi', '$2b$12$24DL2vamA26WKMSwmTuDbelOreWtElQwUgjq8XSPIGISECe3ATfOy', 'pogi', 'ako', 'Member', '2026-02-12 13:07:31');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `vehicle_id` int NOT NULL,
  `brand` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `year` int NOT NULL,
  `license_plate` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `type` enum('Car','Truck','SUV','Van','Motorcycle') COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('Available','Rented','Maintenance') COLLATE utf8mb4_general_ci DEFAULT 'Available',
  `daily_rate` decimal(10,2) NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`vehicle_id`, `brand`, `model`, `year`, `license_plate`, `type`, `status`, `daily_rate`, `image`, `created_at`) VALUES
(1, 'Toyota', 'Vios', 2024, 'ABC 1234', 'Car', 'Available', 1500.00, NULL, '2026-01-20 00:45:12'),
(2, 'Toyota', 'Innova', 2023, 'DEF 5678', 'Van', 'Maintenance', 2500.00, NULL, '2026-01-20 00:45:12'),
(3, 'Toyota', 'Fortuner', 2024, 'GHI 9012', 'SUV', 'Available', 3500.00, NULL, '2026-01-20 00:45:12'),
(4, 'Mitsubishi', 'L300', 2022, 'JKL 3456', 'Truck', 'Available', 2000.00, NULL, '2026-01-20 00:45:12'),
(5, 'Honda', 'Click 125i', 2023, 'MNO 7890', 'Motorcycle', 'Available', 500.00, NULL, '2026-01-20 00:45:12'),
(6, 'Nissan', 'Urvan', 2023, 'PQR 1122', 'Van', 'Available', 2800.00, NULL, '2026-01-20 00:45:12'),
(7, 'Ford', 'Ranger', 2023, 'STU 3344', 'Truck', 'Available', 3000.00, NULL, '2026-01-20 00:45:12'),
(10, 'Toyota', 'Wigo', 2024, 'VWX 5566', 'Car', 'Available', 1200.00, NULL, '2026-01-22 02:23:45');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_logs`
--

CREATE TABLE `vehicle_logs` (
  `log_id` int NOT NULL,
  `vehicle_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `event_type` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `log_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicle_logs`
--

INSERT INTO `vehicle_logs` (`log_id`, `vehicle_id`, `user_id`, `event_type`, `description`, `log_date`) VALUES
(1, 1, 2, 'Return', 'Standard return', '2026-01-20 00:54:56'),
(2, 5, 2, 'Return', 'Standard return', '2026-01-22 02:08:21'),
(3, 2, 2, 'Return', 'returned just fine', '2026-02-12 17:59:05'),
(4, 5, 2, 'Return', 'returned with flat tire', '2026-02-12 17:59:22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`reservation_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD UNIQUE KEY `license_plate` (`license_plate`);

--
-- Indexes for table `vehicle_logs`
--
ALTER TABLE `vehicle_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `reservation_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `vehicle_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `vehicle_logs`
--
ALTER TABLE `vehicle_logs`
  MODIFY `log_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`);

--
-- Constraints for table `vehicle_logs`
--
ALTER TABLE `vehicle_logs`
  ADD CONSTRAINT `vehicle_logs_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`),
  ADD CONSTRAINT `vehicle_logs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
