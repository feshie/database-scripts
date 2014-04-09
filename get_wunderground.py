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
DEFAULT_CONFIG = "database.ini"


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
            return libxml2.parseDoc(urllib.urlopen(
                "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID=%s"% station_id ).read())
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
        logger.setLevel = logging.CRITICAL
    elif options.verbose:
        logger.setLevel = logging.DEBUG
    if options.config_file is None:
        config = DEFAULT_CONFIG
    else:
        config = options.config_file
    logger.debug("Finished parsing arguments")
    get_wunderground(config)

def store_data(location_id, data):
	cursor = db.cursor()
	cursor.execute(""" INSERT IGNORE INTO wunderground_personal_data (location_id, timestamp, description, temperature, humidity, wind_direction, wind_speed,wind_gust_speed, pressure, dewpoint,  heat_index, windchill, solar_radiation, uv, precipitation_1hr, precipitation_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
		 (location_id, data.time, data.description, data.temperature, data.humidity, data.wind_direction, 
			data.wind_speed, data.wind_gust_speed, data.pressure, data.dewpoint, data.heat_index, data.windchill,
			data.solar_radiation, data.uv, data.precipitation_1hr, data.precipitation_day))
	cursor.close()
	db.commit()



def parse_xml(xml):
	data = wundergroundNoaaData()
	try:
		time =  datetime.datetime.strptime(xml.xpathEval('//current_observation/observation_time_rfc822')[0].content, 
				"%a, %d %B %Y %H:%M:%S %Z")
		description = xml.xpathEval('//current_observation/weather')[0].content
		temperature = xml.xpathEval('//current_observation/temp_c')[0].content
		humidity = xml.xpathEval('//current_observation/relative_humidity')[0].content
		wind_direction = xml.xpathEval('//current_observation/wind_degrees')[0].content
		wind_speed =  xml.xpathEval('//current_observation/wind_mph')[0].content
		wind_gust_speed = xml.xpathEval('//current_observation/wind_gust_mph')[0].content
		pressure = xml.xpathEval('//current_observation/pressure_mb')[0].content
		dewpoint = xml.xpathEval('//current_observation/dewpoint_c')[0].content
		heat_index =   xml.xpathEval('//current_observation/heat_index_c')[0].content
		windchill = xml.xpathEval('//current_observation/windchill_c')[0].content
		solar_radiation = xml.xpathEval('//current_observation/solar_radiation')[0].content
		uv = xml.xpathEval('//current_observation/UV')[0].content
		precipitation_1hr = xml.xpathEval('//current_observation/precip_1hr_metric')[0].content
		precipitation_day = xml.xpathEval('//current_observation/precip_today_metric')[0].content
			
		data.time = time

		if description.replace(" ","").isalpha():
			data.description = description
		if is_number(temperature):
			data.temperature = temperature
		if is_number(humidity):
			data.humidity = humidity
		if is_number(wind_direction):
			data.wind_direction = wind_direction
		if is_number(wind_speed):
			data.wind_speed = wind_speed
		if is_number(wind_gust_speed):
			data.wind_gust_speed = wind_gust_speed
		if is_number(pressure):
			data.pressure = pressure
		if is_number(dewpoint):
			data.dewpoint = dewpoint
		if is_number(heat_index):
			data.heat_index = heat_index
		if is_number(windchill):
			data.windchill = windchill
		if is_number(solar_radiation):
			data.solar_radiation = solar_radiation
		if is_number(uv):
			data.uv =uv
		if is_number(precipitation_1hr):
			data.precipitation_1hr = precipitation_1hr
		if is_number(precipitation_day):
			data.precipitation_day = precipitation_day




		return data
	except ValueError, e:
		print "Excepted numbers only"
		print "Error %d %s" % (e.args[0], e.args[1])

class wundergroundNoaaData:
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

def foo():
    try:
        db = MySQLdb.connect(host = db_server, user = db_user, passwd = db_password, db = db_database)
        xml = fetch_xml(id)
        data = parse_xml(xml)
        store_data(id, data)
        time.sleep(5)	
        db.close()
    except MySQLdb.Error, e:
        print "Error %d %s" % (e.args[0], e.args[1])
        sys.exit(1)
