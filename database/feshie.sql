-- phpMyAdmin SQL Dump
-- version 3.3.2deb1ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 31, 2015 at 02:55 PM
-- Server version: 5.1.73
-- PHP Version: 5.3.2-1ubuntu4.29

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `feshie_test`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `accelerometer_converted`
--
CREATE TABLE IF NOT EXISTS `accelerometer_converted` (
`id` int(11)
,`device_id` varchar(40)
,`timestamp` datetime
,`pitch` double(17,0)
,`roll` double(17,0)
);
-- --------------------------------------------------------

--
-- Table structure for table `accelerometer_readings`
--

CREATE TABLE IF NOT EXISTS `accelerometer_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `z` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  KEY `device_id_2` (`device_id`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Raw readings from the acceleromenters' AUTO_INCREMENT=57539 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `adc_described`
--
CREATE TABLE IF NOT EXISTS `adc_described` (
`id` int(11)
,`device_id` varchar(40)
,`timestamp` datetime
,`value` int(11)
,`sensor` varchar(20)
);
-- --------------------------------------------------------

--
-- Table structure for table `adc_ids`
--

CREATE TABLE IF NOT EXISTS `adc_ids` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `adc_mapping`
--

CREATE TABLE IF NOT EXISTS `adc_mapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `adc_id` int(11) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime DEFAULT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `adc_id` (`adc_id`),
  KEY `start` (`start`),
  KEY `end` (`end`),
  KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `adc_names`
--

CREATE TABLE IF NOT EXISTS `adc_names` (
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `adc_readings`
--

CREATE TABLE IF NOT EXISTS `adc_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `adc_id` smallint(6) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`,`adc_id`),
  KEY `adc_id` (`adc_id`),
  KEY `timestamp` (`timestamp`),
  KEY `device_id_2` (`device_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=35104 ;

-- --------------------------------------------------------

--
-- Table structure for table `analog_smart_sensor_readings`
--

CREATE TABLE IF NOT EXISTS `analog_smart_sensor_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `avr_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `a1` float DEFAULT NULL,
  `a2` float DEFAULT NULL,
  `a3` float DEFAULT NULL,
  `a4` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`,`timestamp`),
  KEY `device_id_2` (`device_id`),
  KEY `timestamp` (`timestamp`),
  KEY `avr_id` (`avr_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Data from the AVR analog smart sensors' AUTO_INCREMENT=2284 ;

-- --------------------------------------------------------

--
-- Table structure for table `avr_devices`
--

CREATE TABLE IF NOT EXISTS `avr_devices` (
  `id` int(11) NOT NULL COMMENT 'decimal',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `battery_readings`
--

CREATE TABLE IF NOT EXISTS `battery_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  KEY `device_id_2` (`device_id`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=57548 ;

-- --------------------------------------------------------

--
-- Table structure for table `chain_readings`
--

CREATE TABLE IF NOT EXISTS `chain_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `t1` float DEFAULT NULL COMMENT 'degrees celcius',
  `pitch1` float DEFAULT NULL,
  `roll1` float DEFAULT NULL,
  `t2` float DEFAULT NULL COMMENT 'degrees celcius',
  `pitch2` float DEFAULT NULL,
  `roll2` float DEFAULT NULL,
  `t3` float DEFAULT NULL COMMENT 'degrees celcius',
  `pitch3` float DEFAULT NULL,
  `roll3` float DEFAULT NULL,
  `t4` float DEFAULT NULL COMMENT 'degrees celcius',
  `pitch4` float DEFAULT NULL,
  `roll4` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`,`timestamp`),
  KEY `device_id_2` (`device_id`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=156 ;

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `id` varchar(40) NOT NULL,
  `location` int(11) DEFAULT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `location` (`location`),
  KEY `type` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Stand-in structure for view `device_info`
--
CREATE TABLE IF NOT EXISTS `device_info` (
`id` varchar(40)
,`type` varchar(40)
,`location` varchar(40)
,`latitude` double
,`longitude` double
,`altitude` int(11)
);
-- --------------------------------------------------------

--
-- Table structure for table `device_type`
--

CREATE TABLE IF NOT EXISTS `device_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `dewpoint_readings`
--

CREATE TABLE IF NOT EXISTS `dewpoint_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'degrees celcius',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `feshie_bridge_readings`
--
CREATE TABLE IF NOT EXISTS `feshie_bridge_readings` (
`id` int(11)
,`device` varchar(40)
,`timestamp` datetime
,`value` float
);
-- --------------------------------------------------------

--
-- Table structure for table `humidity_readings`
--

CREATE TABLE IF NOT EXISTS `humidity_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'relative humidity %',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `image_data`
--

CREATE TABLE IF NOT EXISTS `image_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device` (`device`,`timestamp`),
  UNIQUE KEY `filename` (`filename`),
  KEY `device_2` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE IF NOT EXISTS `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `altitude` int(11) DEFAULT NULL COMMENT 'in meters',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `location` (`latitude`,`longitude`,`altitude`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `altitude` (`altitude`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `onewire_devices`
--

CREATE TABLE IF NOT EXISTS `onewire_devices` (
  `id` smallint(6) NOT NULL COMMENT 'decimal',
  `avr_id` int(11) NOT NULL,
  `colour` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `avr_id` (`avr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `onewire_readings`
--

CREATE TABLE IF NOT EXISTS `onewire_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `sensor_id` smallint(6) NOT NULL,
  `value` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id_2` (`device_id`),
  KEY `sensor_id` (`sensor_id`),
  KEY `timestamp` (`timestamp`),
  KEY `device_id` (`timestamp`,`sensor_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=105376 ;

-- --------------------------------------------------------

--
-- Table structure for table `pressure_readings`
--

CREATE TABLE IF NOT EXISTS `pressure_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'mb',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `rain_converted`
--
CREATE TABLE IF NOT EXISTS `rain_converted` (
`device_id` varchar(40)
,`timestamp` datetime
,`mm` decimal(15,4)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `rain_hourly`
--
CREATE TABLE IF NOT EXISTS `rain_hourly` (
`device_id` varchar(40)
,`timestamp` varchar(24)
,`SUM(value)` decimal(32,0)
);
-- --------------------------------------------------------

--
-- Table structure for table `rain_readings`
--

CREATE TABLE IF NOT EXISTS `rain_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` int(11) NOT NULL COMMENT 'Number of ticks',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`),
  KEY `timestamp` (`timestamp`),
  KEY `device_id_2` (`device_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2400 ;

-- --------------------------------------------------------

--
-- Table structure for table `river_depth_readings`
--

CREATE TABLE IF NOT EXISTS `river_depth_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'meters',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device` (`device`,`timestamp`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='River depth in meters' AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `sepa_latest_difference`
--
CREATE TABLE IF NOT EXISTS `sepa_latest_difference` (
`difference` decimal(14,4)
);
-- --------------------------------------------------------

--
-- Table structure for table `temperature_readings`
--

CREATE TABLE IF NOT EXISTS `temperature_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'degrees celcius',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=57547 ;

-- --------------------------------------------------------

--
-- Table structure for table `unprocessed_data`
--

CREATE TABLE IF NOT EXISTS `unprocessed_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` char(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `data` blob NOT NULL,
  `unpacked` tinyint(1) NOT NULL DEFAULT '0',
  `corrupt` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `timestamp` (`timestamp`),
  KEY `unpacked` (`unpacked`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=57792 ;

-- --------------------------------------------------------

--
-- Table structure for table `unprocessed_smart_data`
--

CREATE TABLE IF NOT EXISTS `unprocessed_smart_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `data` blob NOT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  `corrupt` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`,`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=23515 ;

-- --------------------------------------------------------

--
-- Table structure for table `wind_readings`
--

CREATE TABLE IF NOT EXISTS `wind_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `direction` float NOT NULL COMMENT 'degrees',
  `speed` float NOT NULL COMMENT 'mph',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `wunderground_data`
--
CREATE TABLE IF NOT EXISTS `wunderground_data` (
`location` varchar(40)
,`timestamp` datetime
,`temperature` float
,`dewpoint` float
,`humidity` float
,`pressure` float
,`wind_direction` float
,`wind_speed` float
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `wunderground_latest_difference`
--
CREATE TABLE IF NOT EXISTS `wunderground_latest_difference` (
`difference` decimal(14,4)
);
-- --------------------------------------------------------

--
-- Structure for view `accelerometer_converted`
--
DROP TABLE IF EXISTS `accelerometer_converted`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb`@`localhost` SQL SECURITY DEFINER VIEW `accelerometer_converted` AS select `accelerometer_readings`.`id` AS `id`,`accelerometer_readings`.`device_id` AS `device_id`,`accelerometer_readings`.`timestamp` AS `timestamp`,round(((atan(`accelerometer_readings`.`y`,`accelerometer_readings`.`z`) * 180) / pi()),0) AS `pitch`,round(((atan(`accelerometer_readings`.`x`,sqrt(((`accelerometer_readings`.`y` * `accelerometer_readings`.`y`) + (`accelerometer_readings`.`z` * `accelerometer_readings`.`z`)))) * 180) / pi()),0) AS `roll` from `accelerometer_readings` where 1;

-- --------------------------------------------------------

--
-- Structure for view `adc_described`
--
DROP TABLE IF EXISTS `adc_described`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb`@`localhost` SQL SECURITY DEFINER VIEW `adc_described` AS select `a`.`id` AS `id`,`a`.`device_id` AS `device_id`,`a`.`timestamp` AS `timestamp`,`a`.`value` AS `value`,`m`.`name` AS `sensor` from (`adc_readings` `a` left join `adc_mapping` `m` on(((`a`.`device_id` = `m`.`device_id`) and (`a`.`adc_id` = `m`.`adc_id`))));

-- --------------------------------------------------------

--
-- Structure for view `device_info`
--
DROP TABLE IF EXISTS `device_info`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb08r`@`localhost` SQL SECURITY DEFINER VIEW `device_info` AS select `devices`.`id` AS `id`,`device_type`.`name` AS `type`,`locations`.`name` AS `location`,`locations`.`latitude` AS `latitude`,`locations`.`longitude` AS `longitude`,`locations`.`altitude` AS `altitude` from ((`devices` left join `device_type` on((`devices`.`type` = `device_type`.`id`))) left join `locations` on((`devices`.`location` = `locations`.`id`)));

-- --------------------------------------------------------

--
-- Structure for view `feshie_bridge_readings`
--
DROP TABLE IF EXISTS `feshie_bridge_readings`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb08r`@`localhost` SQL SECURITY DEFINER VIEW `feshie_bridge_readings` AS select `river_depth_readings`.`id` AS `id`,`river_depth_readings`.`device` AS `device`,`river_depth_readings`.`timestamp` AS `timestamp`,`river_depth_readings`.`value` AS `value` from `river_depth_readings` where (`river_depth_readings`.`device` like 'Feshie Bridge');

-- --------------------------------------------------------

--
-- Structure for view `rain_converted`
--
DROP TABLE IF EXISTS `rain_converted`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb`@`localhost` SQL SECURITY DEFINER VIEW `rain_converted` AS select `rain_readings`.`device_id` AS `device_id`,`rain_readings`.`timestamp` AS `timestamp`,((`rain_readings`.`value` * 2) / 55) AS `mm` from `rain_readings`;

-- --------------------------------------------------------

--
-- Structure for view `rain_hourly`
--
DROP TABLE IF EXISTS `rain_hourly`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb`@`localhost` SQL SECURITY DEFINER VIEW `rain_hourly` AS select `rain_readings`.`device_id` AS `device_id`,date_format(`rain_readings`.`timestamp`,'%Y-%m-%d %H:00:00') AS `timestamp`,sum(`rain_readings`.`value`) AS `SUM(value)` from `rain_readings` group by cast(`rain_readings`.`timestamp` as date),hour(`rain_readings`.`timestamp`);

-- --------------------------------------------------------

--
-- Structure for view `sepa_latest_difference`
--
DROP TABLE IF EXISTS `sepa_latest_difference`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb08r`@`localhost` SQL SECURITY DEFINER VIEW `sepa_latest_difference` AS select ((unix_timestamp() - unix_timestamp(max(`river_depth_readings`.`timestamp`))) / 60) AS `difference` from `river_depth_readings` where (`river_depth_readings`.`device` = 'Feshie Bridge');

-- --------------------------------------------------------

--
-- Structure for view `wunderground_data`
--
DROP TABLE IF EXISTS `wunderground_data`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb08r`@`localhost` SQL SECURITY DEFINER VIEW `wunderground_data` AS select `device_info`.`location` AS `location`,`t`.`timestamp` AS `timestamp`,`t`.`value` AS `temperature`,`d`.`value` AS `dewpoint`,`h`.`value` AS `humidity`,`p`.`value` AS `pressure`,`w`.`direction` AS `wind_direction`,`w`.`speed` AS `wind_speed` from (((((`temperature_readings` `t` left join `device_info` on((`t`.`device` = `device_info`.`id`))) left join `dewpoint_readings` `d` on(((`t`.`device` = `d`.`device`) and (`t`.`timestamp` = `d`.`timestamp`)))) left join `humidity_readings` `h` on(((`t`.`device` = `h`.`device`) and (`t`.`timestamp` = `h`.`timestamp`)))) left join `pressure_readings` `p` on(((`t`.`device` = `p`.`device`) and (`t`.`timestamp` = `p`.`timestamp`)))) left join `wind_readings` `w` on(((`t`.`device` = `w`.`device`) and (`t`.`timestamp` = `w`.`timestamp`)))) where (`device_info`.`type` = 'wunderground') order by `t`.`timestamp`;

-- --------------------------------------------------------

--
-- Structure for view `wunderground_latest_difference`
--
DROP TABLE IF EXISTS `wunderground_latest_difference`;

CREATE ALGORITHM=UNDEFINED DEFINER=`pjb08r`@`localhost` SQL SECURITY DEFINER VIEW `wunderground_latest_difference` AS select ((unix_timestamp() - unix_timestamp(max(`wunderground_data`.`timestamp`))) / 60) AS `difference` from `wunderground_data`;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adc_readings`
--
ALTER TABLE `adc_readings`
  ADD CONSTRAINT `adc_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`location`) REFERENCES `locations` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `devices_ibfk_2` FOREIGN KEY (`type`) REFERENCES `device_type` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `dewpoint_readings`
--
ALTER TABLE `dewpoint_readings`
  ADD CONSTRAINT `dewpoint_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `humidity_readings`
--
ALTER TABLE `humidity_readings`
  ADD CONSTRAINT `humidity_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `image_data`
--
ALTER TABLE `image_data`
  ADD CONSTRAINT `image_data_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `pressure_readings`
--
ALTER TABLE `pressure_readings`
  ADD CONSTRAINT `pressure_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `river_depth_readings`
--
ALTER TABLE `river_depth_readings`
  ADD CONSTRAINT `river_depth_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `temperature_readings`
--
ALTER TABLE `temperature_readings`
  ADD CONSTRAINT `temperature_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `wind_readings`
--
ALTER TABLE `wind_readings`
  ADD CONSTRAINT `wind_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`);
