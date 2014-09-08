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
            raise FeshieDbError(e.msg)

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
            cursor.execute(
                "INSERT IGNORE INTO river_depth_readings (device, timestamp, value) VALUES ('%s', '%s', %s)",
                (device, timestamp, value))
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

class ConfigError(Exception):
    """
        An error for when something has gone wrong reading the config
    """
    pass

class FeshieDbError(Exception):
    pass
