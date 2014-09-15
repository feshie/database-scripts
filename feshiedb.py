"""
    Basic database tools
"""


from configobj import ConfigObj
import MySQLdb
import logging
class FeshieDb:

    def __init__(self, config_file, logging_level = logging.ERROR):
        self.logger = logging.getLogger("FeshieDb")
        self.logger.setLevel(logging_level)
        self.logger.debug("Loading database config")
        self.db_config = FeshieDbConfig(config_file)
        self.db = None
        self.connect()

    def connect(self):
        host = self.db_config.server
        user = self.db_config.user
        password = self.db_config.password
        database = self.db_config.database
        try:
            db = MySQLdb.connect(host = host, user = user,
                passwd = password, db = database)
            self.logger.info("Connected to database %s on %s" %(database, host))
            self.db = db
        except MySQLdb.Error, e:
            self.logger.critical("Unable to connect to db %s on %s as user %s" %
                (database, host, user))
            self.logger.critical(e)
            raise FeshieDbError(str(e))

    def connected(self):
        return self.db is not None

    def get_wunderground_stations(self):
        self.db.query("SELECT id FROM devices WHERE type = 1")
        result = self.db.store_result()
        rows = result.fetch_row(0)
        return rows

    def get_latest_unprocessed(self):
        if not self.connected():
            raise FeshieDbError() 
        self.db.query("SELECT * FROM `unprocessed_data` WHERE id = (SELECT MAX(id) from `unprocessed_data`);")
        raw =  self.db.store_result().fetch_row()[0]
        return RawReading(raw[1], raw[2], raw[3], bool(raw[4]))
        
        

    def save_temperature(self, device, timestamp, value):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO temperature_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device, timestamp,value))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature stored")

    def save_humidity(self, device, timestamp, value):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                 "INSERT IGNORE INTO humidity_readings (device, timestamp, value) VALUES (%s, %s, %s)",
                (device, timestamp, value))
            cursor.close()
            self.db.commit()

    def save_wind(self, device, timestamp, direction, speed):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                 "INSERT IGNORE INTO wind_readings (device, timestamp, direction, speed) VALUES (%s, %s, %s, %s)",
                (device, timestamp, direction, speed))
            cursor.close()
            self.db.commit()

    def save_pressure(self, device, timestamp, value):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO pressure_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device, timestamp, value))
            cursor.close()
            self.db.commit()


    def save_dewpoint(self, device, timestamp, value):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO dewpoint_readings (device, timestamp,value) VALUES (%s, %s,%s)",
                (device, timestamp, value))
            cursor.close()
            self.db.commit()

    def save_riverdepth(self, device, timestamp, value):
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cmd = ("INSERT IGNORE INTO river_depth_readings (device, timestamp,value) VALUES ('%s', '%s', %s)"% (device, str(timestamp), value))
            self.logger.debug(cmd)
            cursor.execute(cmd)
            cursor.close()
            self.db.commit()


class FeshieDbConfig:
    """
        A class containing the connection information required to access the
        database
    """
    def __init__(self, config_file):
        """
            Read the config file and extract the required information
        """
        try:
            config = ConfigObj(config_file)
            self.database = config["database"]
            self.server = config["server"]
            self.user = config["user"]
            self.password = config["pass"]
        except KeyError:
            raise ConfigError("Invalid config File")    


class RawReading:
    def __init__(self, node, recieved_time, data, processed = False):
        self.node = node
        self.recieved_time = recieved_time
        self.data = data
        self.processed = processed

class ConfigError(Exception):
    """
        An error for when something has gone wrong reading the config
    """
    pass

class FeshieDbError(Exception):
    pass
