-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 02, 2016 at 06:07 PM
-- Server version: 5.5.49-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `feshie`
--

--
-- Dumping data for table `adc_ids`
--

INSERT INTO `adc_ids` (`id`) VALUES
(1),
(2);

--
-- Dumping data for table `adc_names`
--

INSERT INTO `adc_names` (`name`) VALUES
('moisture');

--
-- Dumping data for table `adc_mapping`
--

INSERT INTO `adc_mapping` (`id`, `device_id`, `adc_id`, `start`, `end`, `name`) VALUES
(1, '1099', 1, '2015-03-30 18:11:43', NULL, 'moisture'),
(2, '106b', 1, '2015-06-01 00:00:00', NULL, 'moisture'),
(3, '1058', 1, '2015-06-01 00:00:00', NULL, 'moisture'),
(4, '1064', 1, '2015-06-01 00:00:00', NULL, 'moisture');



--
-- Dumping data for table `avr_devices`
--

INSERT INTO `avr_devices` (`id`) VALUES
(1),
(2),
(16),
(17),
(32),
(33),
(34);

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`id`, `location`, `type`) VALUES
('03063', 1, 1),
('03065', 2, 1),
('03072', 6, 1),
('0fd2', NULL, 3),
('0fda', NULL, 3),
('0fee', NULL, 3),
('1005', NULL, 3),
('1028', NULL, 3),
('1058', NULL, 3),
('105c', NULL, 3),
('1068', NULL, 3),
('106a', NULL, 3),
('106b', NULL, 3),
('107c', NULL, 3),
('1084', NULL, 3),
('1099', NULL, 3),
('10dc', NULL, 3),
('Feshie Bridge', 8, 2),
('IBIRKHAL2', 7, 1),
('IMORAYBA2', 4, 1),
('ISCOTLAN102', 5, 1),
('ISCOTLAN99', 3, 1);

--
-- Dumping data for table `device_names`
--

INSERT INTO `device_names` (`id`, `device_id`, `name`, `start_date`, `end_date`) VALUES
(1, '107c', 'Router 1', '2015-07-01 00:00:00', NULL),
(2, '105c', 'Router 2', '2015-07-01 00:00:00', NULL),
(3, '106b', 'Peat', '2015-07-01 00:00:00', NULL),
(4, '1068', 'Lochan', '2015-07-01 00:00:00', NULL),
(5, '1099', 'Hummock', '2015-07-01 00:00:00', NULL),
(6, '1084', 'Turf', '2015-07-01 00:00:00', NULL),
(7, '106a', 'Router 3', '2015-07-03 14:00:00', NULL),
(9, '1058', 'Stream', '2015-07-05 11:00:00', NULL);

--
-- Dumping data for table `device_type`
--

INSERT INTO `device_type` (`id`, `name`) VALUES
(4, 'Muntjack'),
(2, 'sepa'),
(1, 'wunderground'),
(3, 'Z1');

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `name`, `latitude`, `longitude`, `altitude`) VALUES
(1, 'Wunderground Aviemore', 57.21, -3.83, 228),
(2, 'Wunderground Caingorm', 57.12, -3.64, 1237),
(3, 'Wunderground Nethy Bridge', 57.26, -3.65, 232),
(4, 'Wunderground Glenlivet', 57.312, -3.408, 0),
(5, 'Wunderground Carrbridge', 57.283, -3.827, 279),
(6, 'Wunderground Cairnwell', 56.88, -3.42, 928),
(7, 'Wundergroun Birkhall', 57.041, -3.07, 252),
(8, 'Feshie Bridge', 57.11878, -3.902497, 232);

--
-- Dumping data for table `onewire_devices`
--

INSERT INTO `onewire_devices` (`id`, `avr_id`, `colour`) VALUES
(4, 17, 'Red'),
(10, 17, 'Green'),
(30, 16, 'Blue'),
(49, 16, 'Red'),
(68, 17, 'White'),
(130, 16, 'Yellow'),
(204, 17, 'Blue'),
(220, 17, 'Yellow'),
(227, 16, 'White'),
(251, 16, 'Green');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
