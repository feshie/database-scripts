#!/usr/bin/env python
import logging 
from optparse import OptionParser,OptionGroup  
#has to run on a server with python 2.6 so argparse is not an option

import libxml2
import urllib


import MySQLdb
import sys
import time
import datetime
from dateutil.tz import *

import feshiedb

LOG_LEVEL = logging.ERROR
DEFAULT_CONFIG = "db.ini"


#IDs that are in the database but are no longer valid so whould be ignored
#for data collection purposes
IGNORE_IDS = []

def is_number(s):
	try:
		float(s)
		ret = True
	except ValueError:
		ret = False	
	return ret


class XmlError(Exception):
    pass

class WundergroundNoaaData:
    """represents data from wunderground noaa nodes"""
    def __init__(self):
        self.time = None
        self.description = None
        self.temperature = None
        self.humidity = None
        self.wind_direction = None
        self.wind_speed = None
        self.wind_gust_speed = None
        self.pressure = None
        self.dewpoint = None
        self.heat_index = None
        self.windchill = None
        self.solar_radiation = None
        self.uv = None
        self.precipitation_1hr = None
        self.precipitation_day = None

class WundergroundFetcher:


    def __init__(self, config, logging_level):
        logging.basicConfig()
        self.logger = logging.getLogger("WundergroundFetcher")
        self.logger.setLevel(logging_level)
        self.logger.debug("Loading database config")
        self.db = self.__dbconnect(feshiedb.FeshieDb(config))


    def __dbconnect(self, db_config):
        host = db_config.server
        user = db_config.user
        password = db_config.password
        database = db_config.database
        try:
            db = MySQLdb.connect(host = host, user = user, passwd = password, db = database)
            self.logger.info("Connected to database %s on %s" %(database, host))
            return db
        except MySQLdb.Error, e:
            self.logger.critical("Unable to connect to db %s on %s as user %s" %
                (database, host, user))
            return None


    def fetch_xml(self, station_id):
        try:
            url = "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID=%s"% station_id
            self.logger.debug("Fetching: %s" % url)
            return libxml2.parseDoc(urllib.urlopen(url).read())
        except Error, e:
            self.logger.error( "An error occured when getting the xml")
            self.logger.error("Error %d %s" % (e.args[0], e.args[1]))
            raise XmlError()



    def get_stations(self):
        self.db.query("SELECT id FROM devices WHERE type = 1")
        result = self.db.store_result()
        rows = result.fetch_row(0)
        clean = []
        for row in rows:
            id = row[0]
            if id in IGNORE_IDS:
                self.logger.debug("Rejecting %s" % id)
                continue
            else:
                clean.append(id)
                self.logger.debug("Adding %s" % id)
        return clean


    def fetch_all_stations(self):
        stations = self.get_stations()
        for s in stations:
            self.logger.debug("Processing %s" % s)
            try:
                xml = self.fetch_xml(s)
                data = self.parse_xml(xml)
                self.store_data(s, data)
            except Exception, e:
                print e
                continue #Try the next station


    def parse_xml(self, xml):
        data = WundergroundNoaaData()
        time =  datetime.datetime.strptime(xml.xpathEval('//current_observation/observation_time_rfc822')[0].content, 
                "%a, %d %b %Y %H:%M:%S %Z")
        #description = xml.xpathEval('//current_observation/weather')[0].content
        temperature = xml.xpathEval('//current_observation/temp_c')[0].content
        humidity = xml.xpathEval('//current_observation/relative_humidity')[0].content
        wind_direction = xml.xpathEval('//current_observation/wind_degrees')[0].content
        wind_speed =  xml.xpathEval('//current_observation/wind_mph')[0].content
        #wind_gust_speed = xml.xpathEval('//current_observation/wind_gust_mph')[0].content
        pressure = xml.xpathEval('//current_observation/pressure_mb')[0].content
        dewpoint = xml.xpathEval('//current_observation/dewpoint_c')[0].content
        #heat_index =   xml.xpathEval('//current_observation/heat_index_c')[0].content
        #windchill = xml.xpathEval('//current_observation/windchill_c')[0].content
        #solar_radiation = xml.xpathEval('//current_observation/solar_radiation')[0].content
        #uv = xml.xpathEval('//current_observation/UV')[0].content
        #precipitation_1hr = xml.xpathEval('//current_observation/precip_1hr_metric')[0].content
        #precipitation_day = xml.xpathEval('//current_observation/precip_today_metric')[0].content
            
        data.time = time

        #if description.replace(" ","").isalpha():
        #    data.description = description
        if is_number(temperature):
            data.temperature = temperature
            self.logger.debug("Temperature = %s" % temperature)
        else:
            self.logger.error("Temperature is not a number: %s" % temperature)
        humidity = humidity.strip("%")
        if is_number(humidity):
            data.humidity = humidity
            self.logger.debug("Humidity = %s" % humidity)
        else:
            self.logger.error("Humidity is not a number: %s" % humidity)
        if is_number(wind_direction):
            data.wind_direction = wind_direction
            self.logger.debug("Wind direction = %s" % wind_direction)
        else:
            self.logger.error("Wind dir is not a number: %s" % wind_dirction)
        if is_number(wind_speed):
            data.wind_speed = wind_speed
            self.logger.debug("Wind speed = %s" % wind_speed)
        else:
            self.logger.error("Wind speed in not a number: %s" % wind_speed)
        #if is_number(wind_gust_speed):
        #    data.wind_gust_speed = wind_gust_speed
        if is_number(pressure):
            data.pressure = pressure
            self.logger.debug("Pressue = %s" % pressure)
        else:
            self.logger.error("Pressure is not a number: %s" % pressure)
        if is_number(dewpoint):
            data.dewpoint = dewpoint
            self.logger.debug("Dewpoint = %s" % dewpoint)
        else:
            self.logger.error("Dewpoint is not a number: %s" % dewpoint)
        #if is_number(heat_index):
        #    data.heat_index = heat_index
        #if is_number(windchill):
        #    data.windchill = windchill
        #if is_number(solar_radiation):
        #    data.solar_radiation = solar_radiation
        #if is_number(uv):
        #    data.uv =uv
        #if is_number(precipitation_1hr):
        #    data.precipitation_1hr = precipitation_1hr
        #if is_number(precipitation_day):
        #    data.precipitation_day = precipitation_day
        return data
    
    def store_data(self, location_id, data):
        cursor = self.db.cursor()
        if data.temperature is not None:
            cursor.execute("""INSERT IGNORE INTO temperature_readings (device, timestamp, value) VALUES (%s, %s, %s)""",
                (location_id, data.time, data.temperature))
        if data.humidity is not None:
            cursor.execute("INSERT IGNORE INTO humidity_readings (device, timestamp, value) VALUES (%s, %s, %s)",
                (location_id, data.time, data.humidity))
        if data.wind_direction is not None and data.wind_speed is not None:
            cursor.execute("INSERT IGNORE INTO wind_readings (device, timestamp, direction, speed) VALUES (%s, %s, %s, %s)",
                (location_id, data.time, data.wind_direction, data.wind_speed))
        if data.pressure is not None:
            cursor.execute("INSERT IGNORE INTO pressure_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (location_id, data.time, data.pressure))
        if data.dewpoint is not None:
            cursor.execute("INSERT IGNORE INTO dewpoint_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (location_id, data.time, data.dewpoint))
        cursor.close()
        self.db.commit()
        self.logger.debug("Data saved for station %s" % location_id)

if __name__ == "__main__":
    parser = OptionParser()
    group = OptionGroup(parser, "Verbosity Options",
        "Options to change the level of output")
    group.add_option("-q", "--quiet", action="store_true",
         dest="quiet", default=False,
    help="Supress all but critical errors")
    group.add_option("-v", "--verbose", action="store_true",
        dest="verbose", default=False,
        help="Print all information available")
    parser.add_option_group(group)
    parser.add_option("-c", "--config", action="store",
    type="string", dest="config_file",
    help="Config file containing database credentials")
    (options, args) = parser.parse_args()
    if options.quiet:
        log_level = logging.CRITICAL
    elif options.verbose:
        log_level = logging.DEBUG
    if options.config_file is None:
        config = DEFAULT_CONFIG
    else:
        config = options.config_file
    w = WundergroundFetcher(config, log_level)
    w.fetch_all_stations()




