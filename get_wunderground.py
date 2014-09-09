#!/usr/bin/env python
"""
    Fetchs data from the wunderground api and stores it in the database
    When runs as a commandline script will get data for all devices in 
    the database
"""
import logging 
from optparse import OptionParser, OptionGroup  
#has to run on a server with python 2.6 so argparse is not an option

import libxml2
import urllib
import MySQLdb
import datetime

import feshiedb

DEFAULT_LOG_LEVEL = logging.ERROR
DEFAULT_CONFIG = "db.ini"


#IDs that are in the database but are no longer valid so whould be ignored
#for data collection purposes
IGNORE_IDS = []

def is_number(s):
    """
        Checks to see if a string is a number of if there is something
        preventing a conversion to float
    """
    try:
        float(s)
        ret = True
    except ValueError:
        ret = False 
    return ret


class XmlError(Exception):
    """
        Error type for if something goes wrong fetching the XML
    """
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
    """
        This class actually does the work of getting the data and storing it
    """

    def __init__(self, config_file, logging_level):
        logging.basicConfig()
        self.logger = logging.getLogger("WundergroundFetcher")
        self.logger.setLevel(logging_level)
        self.logger.debug("Loading database config")
        self.db = feshiedb.FeshieDb(config_file, logging_level)
        if not self.db.connected():
            self.logger.critical("No database connection")
            exit(1)

    def fetch_xml(self, station_id):
        try:
            url = "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID=%s"% station_id
            self.logger.debug("Fetching: %s" % url)
            return libxml2.parseDoc(urllib.urlopen(url).read())
        except XmlError, e:
            self.logger.error( "An error occured when getting the xml")
            self.logger.error("Error %d %s" % (e.args[0], e.args[1]))
            raise XmlError()



    def get_stations(self):
        rows = self.db.get_wunderground_stations()
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
                self.logger.error(e)
                continue #Try the next station


    def parse_xml(self, xml):
        data = WundergroundNoaaData()
        time =  datetime.datetime.strptime(
            xml.xpathEval('//current_observation/observation_time_rfc822')[0].content, 
            "%a, %d %b %Y %H:%M:%S %Z")
        temperature = xml.xpathEval('//current_observation/temp_c')[0].content
        humidity = xml.xpathEval(
            '//current_observation/relative_humidity')[0].content
        wind_direction = xml.xpathEval(
            '//current_observation/wind_degrees')[0].content
        wind_speed =  xml.xpathEval(
            '//current_observation/wind_mph')[0].content
        pressure = xml.xpathEval('//current_observation/pressure_mb')[0].content
        dewpoint = xml.xpathEval('//current_observation/dewpoint_c')[0].content
            
        data.time = time
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
            self.logger.error("Wind dir is not a number: %s" % wind_direction)
        if is_number(wind_speed):
            data.wind_speed = wind_speed
            self.logger.debug("Wind speed = %s" % wind_speed)
        else:
            self.logger.error("Wind speed in not a number: %s" % wind_speed)
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
        return data
    
    def store_data(self, location_id, data):
        if data.temperature is not None:
            self.db.save_temperature(location_id, data.time, data.temperature) 
        if data.humidity is not None:
                self.db.save_humidity(location_id, data.time, data.humidity)
        if data.wind_direction is not None and data.wind_speed is not None:
                self.db.save_wind(location_id, data.time, data.wind_direction, data.wind_speed)
        if data.pressure is not None:
                self.db.save_pressure(location_id, data.time, data.pressure)
        if data.dewpoint is not None:
                self.db.save_dewpoint(location_id, data.time, data.dewpoint)
        self.logger.debug("Data saved for station %s" % location_id)

if __name__ == "__main__":
    LOG_LEVEL = DEFAULT_LOG_LEVEL
    PARSER = OptionParser()
    GROUP = OptionGroup(PARSER, "Verbosity Options",
        "Options to change the level of output")
    GROUP.add_option("-q", "--quiet", action="store_true",
         dest="quiet", default=False,
    help="Supress all but critical errors")
    GROUP.add_option("-v", "--verbose", action="store_true",
        dest="verbose", default=False,
        help="Print all information available")
    PARSER.add_option_group(GROUP)
    PARSER.add_option("-c", "--config", action="store",
    type="string", dest="config_file",
    help="Config file containing database credentials")
    (OPTIONS, ARGS) = PARSER.parse_args()
    if OPTIONS.quiet:
        LOG_LEVEL = logging.CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = logging.DEBUG
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG
    else:
        CONFIG = OPTIONS.config_file
    FETCHER = WundergroundFetcher(CONFIG, LOG_LEVEL)
    FETCHER.fetch_all_stations()




