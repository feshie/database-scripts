-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 02, 2016 at 06:04 PM
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

-- --------------------------------------------------------

--
-- Stand-in structure for view `1068_20_water_depth`
--
CREATE TABLE IF NOT EXISTS `1068_20_water_depth` (
`timestamp` datetime
,`depth` double(17,0)
);
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Raw readings from the acceleromenters' AUTO_INCREMENT=89331 ;

--
-- RELATIONS FOR TABLE `accelerometer_readings`:
--   `device_id`
--       `devices` -> `id`
--

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
  `id` int(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `adc_mapping`
--

CREATE TABLE IF NOT EXISTS `adc_mapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `adc_id` int(6) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime DEFAULT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `adc_id` (`adc_id`),
  KEY `start` (`start`),
  KEY `end` (`end`),
  KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- RELATIONS FOR TABLE `adc_mapping`:
--   `name`
--       `adc_names` -> `name`
--   `adc_id`
--       `adc_ids` -> `id`
--

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
  `adc_id` int(6) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`,`timestamp`,`adc_id`),
  KEY `adc_id` (`adc_id`),
  KEY `timestamp` (`timestamp`),
  KEY `device_id_2` (`device_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31117 ;

--
-- RELATIONS FOR TABLE `adc_readings`:
--   `adc_id`
--       `adc_ids` -> `id`
--   `device_id`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `analog_smart_sensor_readings`
--

CREATE TABLE IF NOT EXISTS `analog_smart_sensor_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `avr_id` int(11) DEFAULT NULL,
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Data from the AVR analog smart sensors' AUTO_INCREMENT=14706 ;

--
-- RELATIONS FOR TABLE `analog_smart_sensor_readings`:
--   `device_id`
--       `devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=89332 ;

--
-- RELATIONS FOR TABLE `battery_readings`:
--   `device_id`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `battery_readings_corrected`
--
CREATE TABLE IF NOT EXISTS `battery_readings_corrected` (
`device_id` varchar(40)
,`timestamp` datetime
,`value` double
);
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7421 ;

--
-- RELATIONS FOR TABLE `chain_readings`:
--   `device_id`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `chain_temperatures`
--
CREATE TABLE IF NOT EXISTS `chain_temperatures` (
`device_id` varchar(40)
,`timestamp` datetime
,`ambient` float
,`t1` float
,`t2` float
,`t3` float
,`t4` float
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `current_names`
--
CREATE TABLE IF NOT EXISTS `current_names` (
`device_id` varchar(40)
,`name` varchar(40)
);
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

--
-- RELATIONS FOR TABLE `devices`:
--   `location`
--       `locations` -> `id`
--   `type`
--       `device_type` -> `id`
--

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
-- Table structure for table `device_names`
--

CREATE TABLE IF NOT EXISTS `device_names` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id_2` (`device_id`,`start_date`),
  KEY `name` (`name`),
  KEY `device_id` (`device_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Used to map ''friendly names'' to device IDs' AUTO_INCREMENT=10 ;

--
-- RELATIONS FOR TABLE `device_names`:
--   `device_id`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `device_type`
--

CREATE TABLE IF NOT EXISTS `device_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
    `node` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=402981 ;

--
-- RELATIONS FOR TABLE `dewpoint_readings`:
--   `device`
--       `devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=402984 ;

--
-- RELATIONS FOR TABLE `humidity_readings`:
--   `device`
--       `devices` -> `id`
--

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

--
-- RELATIONS FOR TABLE `image_data`:
--   `device`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `latest_node_readings`
--
CREATE TABLE IF NOT EXISTS `latest_node_readings` (
`device` varchar(40)
,`name` varchar(40)
,`timestamp` datetime
);
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

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

--
-- RELATIONS FOR TABLE `onewire_devices`:
--   `avr_id`
--       `avr_devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=138772 ;

--
-- RELATIONS FOR TABLE `onewire_readings`:
--   `sensor_id`
--       `onewire_devices` -> `id`
--   `device_id`
--       `devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=338860 ;

--
-- RELATIONS FOR TABLE `pressure_readings`:
--   `device`
--       `devices` -> `id`
--

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
,`value` decimal(32,0)
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=21406 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='River depth in meters' AUTO_INCREMENT=809758 ;

--
-- RELATIONS FOR TABLE `river_depth_readings`:
--   `device`
--       `devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=582875 ;

--
-- RELATIONS FOR TABLE `temperature_readings`:
--   `device`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `unprocessed_data`
--

CREATE TABLE IF NOT EXISTS `unprocessed_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `data` blob NOT NULL,
  `unpacked` tinyint(1) NOT NULL DEFAULT '0',
  `corrupt` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `timestamp` (`timestamp`),
  KEY `unpacked` (`unpacked`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=94625 ;

--
-- RELATIONS FOR TABLE `unprocessed_data`:
--   `device_id`
--       `devices` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `unprocessed_smart_data`
--

CREATE TABLE IF NOT EXISTS `unprocessed_smart_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(40) NOT NULL,
  `timestamp` datetime NOT NULL,
  `data` blob NOT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0',
  `corrupt` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`,`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=60410 ;

--
-- RELATIONS FOR TABLE `unprocessed_smart_data`:
--   `device_id`
--       `devices` -> `id`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=443274 ;

--
-- RELATIONS FOR TABLE `wind_readings`:
--   `device`
--       `devices` -> `id`
--

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
-- Structure for view `1068_20_water_depth`
--
DROP TABLE IF EXISTS `1068_20_water_depth`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `1068_20_water_depth` AS select `analog_smart_sensor_readings`.`timestamp` AS `timestamp`,round((((((`analog_smart_sensor_readings`.`a1` + 81.6876) / 99.559) - ((`analog_smart_sensor_readings`.`a2` + 7493.446) / 105.8817)) * 10.19744) + 10),0) AS `depth` from `analog_smart_sensor_readings`;

-- --------------------------------------------------------

--
-- Structure for view `accelerometer_converted`
--
DROP TABLE IF EXISTS `accelerometer_converted`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `accelerometer_converted` AS select `accelerometer_readings`.`id` AS `id`,`accelerometer_readings`.`device_id` AS `device_id`,`accelerometer_readings`.`timestamp` AS `timestamp`,round(((atan(`accelerometer_readings`.`y`,`accelerometer_readings`.`z`) * 180) / pi()),0) AS `pitch`,round(((atan(`accelerometer_readings`.`x`,sqrt(((`accelerometer_readings`.`y` * `accelerometer_readings`.`y`) + (`accelerometer_readings`.`z` * `accelerometer_readings`.`z`)))) * 180) / pi()),0) AS `roll` from `accelerometer_readings` where 1;

-- --------------------------------------------------------

--
-- Structure for view `adc_described`
--
DROP TABLE IF EXISTS `adc_described`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `adc_described` AS select `a`.`id` AS `id`,`a`.`device_id` AS `device_id`,`a`.`timestamp` AS `timestamp`,`a`.`value` AS `value`,`m`.`name` AS `sensor` from (`adc_readings` `a` left join `adc_mapping` `m` on(((`a`.`device_id` = `m`.`device_id`) and (`a`.`adc_id` = `m`.`adc_id`))));

-- --------------------------------------------------------

--
-- Structure for view `battery_readings_corrected`
--
DROP TABLE IF EXISTS `battery_readings_corrected`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `battery_readings_corrected` AS select `battery_readings`.`device_id` AS `device_id`,`battery_readings`.`timestamp` AS `timestamp`,((`battery_readings`.`value` * 1.4417) - 0.2532) AS `value` from `battery_readings`;

-- --------------------------------------------------------

--
-- Structure for view `chain_temperatures`
--
DROP TABLE IF EXISTS `chain_temperatures`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `chain_temperatures` AS select `t`.`device` AS `device_id`,`t`.`timestamp` AS `timestamp`,`t`.`value` AS `ambient`,`c`.`t1` AS `t1`,`c`.`t2` AS `t2`,`c`.`t3` AS `t3`,`c`.`t4` AS `t4` from (`temperature_readings` `t` left join `chain_readings` `c` on(((`t`.`device` = `c`.`device_id`) and (`t`.`timestamp` = `c`.`timestamp`)))) where `t`.`device` in (select `c`.`device_id` from `devices` where (`devices`.`type` = 3));

-- --------------------------------------------------------

--
-- Structure for view `current_names`
--
DROP TABLE IF EXISTS `current_names`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `current_names` AS select `device_names`.`device_id` AS `device_id`,`device_names`.`name` AS `name` from `device_names` where isnull(`device_names`.`end_date`);

-- --------------------------------------------------------

--
-- Structure for view `device_info`
--
DROP TABLE IF EXISTS `device_info`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `device_info`  AS  select `devices`.`id` AS `id`,`device_type`.`name` AS `type`,`locations`.`name` AS `location`,`locations`.`latitude` AS `latitude`,`locations`.`longitude` AS `longitude`,`locations`.`altitude` AS `altitude`,`device_type`.`node` AS `node` from ((`devices` left join `device_type` on((`devices`.`type` = `device_type`.`id`))) left join `locations` on((`devices`.`location` = `locations`.`id`))) ;


-- --------------------------------------------------------

--
-- Structure for view `feshie_bridge_readings`
--
DROP TABLE IF EXISTS `feshie_bridge_readings`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `feshie_bridge_readings` AS select `river_depth_readings`.`id` AS `id`,`river_depth_readings`.`device` AS `device`,`river_depth_readings`.`timestamp` AS `timestamp`,`river_depth_readings`.`value` AS `value` from `river_depth_readings` where (`river_depth_readings`.`device` like 'Feshie Bridge');

-- --------------------------------------------------------

--
-- Structure for view `latest_node_readings`
--
DROP TABLE IF EXISTS `latest_node_readings`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `latest_node_readings`  AS  select `temperature_readings`.`device` AS `device`,`device_names`.`name` AS `name`,max(`temperature_readings`.`timestamp`) AS `timestamp` from (`temperature_readings` left join `device_names` on((`temperature_readings`.`device` = `device_names`.`device_id`))) where ((`temperature_readings`.`timestamp` <= now()) and `temperature_readings`.`device` in (select `device_info`.`id` from `device_info` where (`device_info`.`node` = 1))) group by `temperature_readings`.`device` order by max(`temperature_readings`.`timestamp`) desc ;


-- --------------------------------------------------------

--
-- Structure for view `rain_converted`
--
DROP TABLE IF EXISTS `rain_converted`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rain_converted` AS select `rain_readings`.`device_id` AS `device_id`,`rain_readings`.`timestamp` AS `timestamp`,((`rain_readings`.`value` * 2) / 55) AS `mm` from `rain_readings`;

-- --------------------------------------------------------

--
-- Structure for view `rain_hourly`
--
DROP TABLE IF EXISTS `rain_hourly`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `rain_hourly` AS select `rain_readings`.`device_id` AS `device_id`,date_format(`rain_readings`.`timestamp`,'%Y-%m-%d %H:00:00') AS `timestamp`,sum(`rain_readings`.`value`) AS `value` from `rain_readings` group by cast(`rain_readings`.`timestamp` as date),hour(`rain_readings`.`timestamp`);

-- --------------------------------------------------------

--
-- Structure for view `sepa_latest_difference`
--
DROP TABLE IF EXISTS `sepa_latest_difference`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `sepa_latest_difference` AS select ((unix_timestamp() - unix_timestamp(max(`river_depth_readings`.`timestamp`))) / 60) AS `difference` from `river_depth_readings` where (`river_depth_readings`.`device` = 'Feshie Bridge');

-- --------------------------------------------------------

--
-- Structure for view `wunderground_data`
--
DROP TABLE IF EXISTS `wunderground_data`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `wunderground_data` AS select `device_info`.`location` AS `location`,`t`.`timestamp` AS `timestamp`,`t`.`value` AS `temperature`,`d`.`value` AS `dewpoint`,`h`.`value` AS `humidity`,`p`.`value` AS `pressure`,`w`.`direction` AS `wind_direction`,`w`.`speed` AS `wind_speed` from (((((`temperature_readings` `t` left join `device_info` on((`t`.`device` = `device_info`.`id`))) left join `dewpoint_readings` `d` on(((`t`.`device` = `d`.`device`) and (`t`.`timestamp` = `d`.`timestamp`)))) left join `humidity_readings` `h` on(((`t`.`device` = `h`.`device`) and (`t`.`timestamp` = `h`.`timestamp`)))) left join `pressure_readings` `p` on(((`t`.`device` = `p`.`device`) and (`t`.`timestamp` = `p`.`timestamp`)))) left join `wind_readings` `w` on(((`t`.`device` = `w`.`device`) and (`t`.`timestamp` = `w`.`timestamp`)))) where (`device_info`.`type` = 'wunderground') order by `t`.`timestamp`;

-- --------------------------------------------------------

--
-- Structure for view `wunderground_latest_difference`
--
DROP TABLE IF EXISTS `wunderground_latest_difference`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `wunderground_latest_difference` AS select ((unix_timestamp() - unix_timestamp(max(`wunderground_data`.`timestamp`))) / 60) AS `difference` from `wunderground_data`;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accelerometer_readings`
--
ALTER TABLE `accelerometer_readings`
  ADD CONSTRAINT `accelerometer_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `adc_mapping`
--
ALTER TABLE `adc_mapping`
  ADD CONSTRAINT `adc_mapping_ibfk_2` FOREIGN KEY (`name`) REFERENCES `adc_names` (`name`) ON UPDATE CASCADE,
  ADD CONSTRAINT `adc_mapping_ibfk_1` FOREIGN KEY (`adc_id`) REFERENCES `adc_ids` (`id`) ON UPDATE CASCADE;
  ADD CONSTRAINT `adc_mapping_ibfk_3` FOREIGN KEY ( `device_id` ) REFERENCES `feshie`.`devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE ;

--
-- Constraints for table `adc_readings`
--
ALTER TABLE `adc_readings`
  ADD CONSTRAINT `adc_readings_ibfk_2` FOREIGN KEY (`adc_id`) REFERENCES `adc_ids` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `adc_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `analog_smart_sensor_readings`
--
ALTER TABLE `analog_smart_sensor_readings`
  ADD CONSTRAINT `analog_smart_sensor_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `battery_readings`
--
ALTER TABLE `battery_readings`
  ADD CONSTRAINT `battery_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `chain_readings`
--
ALTER TABLE `chain_readings`
  ADD CONSTRAINT `chain_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `device_names`
--
ALTER TABLE `device_names`
  ADD CONSTRAINT `device_names_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

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
-- Constraints for table `onewire_devices`
--
ALTER TABLE `onewire_devices`
  ADD CONSTRAINT `onewire_devices_ibfk_1` FOREIGN KEY (`avr_id`) REFERENCES `avr_devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `onewire_readings`
--
ALTER TABLE `onewire_readings`
  ADD CONSTRAINT `onewire_readings_ibfk_2` FOREIGN KEY (`sensor_id`) REFERENCES `onewire_devices` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `onewire_readings_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `pressure_readings`
--
ALTER TABLE `pressure_readings`
  ADD CONSTRAINT `pressure_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `rain_readings`
--
ALTER TABLE `rain_readings` ADD FOREIGN KEY ( `device_id` ) REFERENCES `feshie`.`devices` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE ;

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
-- Constraints for table `unprocessed_data`
--
ALTER TABLE `unprocessed_data`
  ADD CONSTRAINT `unprocessed_data_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `unprocessed_smart_data`
--
ALTER TABLE `unprocessed_smart_data`
  ADD CONSTRAINT `unprocessed_smart_data_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `wind_readings`
--
ALTER TABLE `wind_readings`
  ADD CONSTRAINT `wind_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
