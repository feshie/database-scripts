"""
    Basic database tools
"""




from configobj import ConfigObj
import MySQLdb
import logging

DATE_LIMIT = "2014-01-01 00:00:00"

class FeshieDb(object):


    def __init__(self, config_file, logging_level=logging.ERROR):
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
            db = MySQLdb.connect(
                host=host, user=user,
                passwd=password, db=database)
            self.logger.info("Connected to database %s on %s", database, host)
            self.db = db
        except MySQLdb.Error, e:
            self.logger.critical(
                "Unable to connect to db %s on %s as user %s",
                database, host, user)
            self.logger.critical(e)
            raise FeshieDbError(str(e))

    def connected(self):
        return self.db is not None

    def get_z1_nodes(self):
        return self.get_nodes()

    def get_nodes(self):
        if not self.connected():
            raise FeshieDbError()
        self.db.query("SELECT id FROM device_info WHERE node = 1")
        result = self.db.store_result()
        rows = result.fetch_row(0)
        nodes = []
        for row in rows:
            nodes.append(row[0])
        return nodes

    def get_wunderground_stations(self):
        self.db.query("SELECT id FROM devices WHERE type = 1")
        result = self.db.store_result()
        rows = result.fetch_row(0)
        return rows

    def get_latest_unprocessed(self):
        if not self.connected():
            raise FeshieDbError()
        self.db.query("SELECT id, device_id, timestamp, HEX(data), unpacked FROM `unprocessed_data` WHERE id = (SELECT MAX(id) from `unprocessed_data`);")
        raw = self.db.store_result().fetch_row()[0]
        return RawReading(raw[0], raw[1], raw[2], raw[3], bool(raw[4]))

    def get_all_unprocessed(self):
        if not self.connected():
            raise FeshieDbError()

        self.db.query("SELECT id, device_id, timestamp, HEX(data), unpacked FROM `unprocessed_data` WHERE unpacked = 0;")
        raw = self.db.store_result().fetch_row(maxrows=0)
        data = []
        for i in raw:
            data.append(RawReading(i[0], i[1], i[2], i[3], bool(i[4])))
        return data

    def get_all_unprocessed_smart(self):
        if not self.connected():
            raise FeshieDbError()
        self.db.query("SELECT id, device_id, timestamp, HEX(data), processed FROM `unprocessed_smart_data` WHERE processed = 0;")
        raw = self.db.store_result().fetch_row(maxrows=0)
        data = []
        for i in raw:
            data.append(RawSmartReading(i[0], i[1], i[2], i[3], bool(i[4])))
        return data

    def mark_smart_processed(self, id):
        self.logger.debug("Marking smart data as processed")
        if not self.connected():
            raise FeshieDbError()
        cursor = self.db.cursor()
        cursor.execute("UPDATE unprocessed_smart_data SET processed = 1 WHERE id = %s;", (id,))
        cursor.close()
        self.db.commit()
        self.logger.debug("Marked %s as processed", id)

    def mark_smart_corrupt(self, id):
        self.logger.debug("Marking smart data corrupt")
        if not self.connected():
            raise FeshieDbError()
        cursor = self.db.cursor()
        cursor.execute("UPDATE unprocessed_smart_data SET corrupt = 1 WHERE id = %s;", (id,))
        cursor.close()
        self.db.commit()
        self.logger.debug("Marked %s as corrupt", id)

    def mark_processed(self, id):
        self.logger.debug("Marking processed")
        if not self.connected():
            raise FeshieDbError()
        cursor = self.db.cursor()
        cursor.execute("UPDATE unprocessed_data SET unpacked = 1 WHERE id = %s;", (id,))
        cursor.close()
        self.db.commit()
        self.logger.debug("Marked %s as processed", id)

    def mark_corrupt(self, id):
        self.logger.debug("Marking corrupt")
        if not self.connected():
            raise FeshieDbError()
        cursor = self.db.cursor()
        cursor.execute("UPDATE unprocessed_data SET corrupt = 1 WHERE id = %s;", (id,))
        cursor.close()
        self.db.commit()
        self.logger.debug("Marked %s as corrupt", id)

    def get_sepa_difference(self):
        if not self.connected():
            raise FeshieDbError()
        self.db.query("SELECT * FROM sepa_latest_difference;")
        raw = self.db.store_result().fetch_row()[0]
        return raw[0]

    def get_wunderground_difference(self):
        if not self.connected():
            raise FeshieDbError()
        self.db.query("SELECT * FROM wunderground_latest_difference;")
        raw = self.db.store_result().fetch_row()[0]
        return raw[0]


    def save_temperature(self, device, timestamp, value):
        self.logger.debug("Saving temperature")
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT IGNORE INTO temperature_readings (device, timestamp,value) VALUES (%s, %s, %s)",
                (device, timestamp, value))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature stored")

    def update_temperature(self, device, timestamp, value):
        self.logger.debug("Updating temperature")
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE temperature_readings SET value = %s WHERE device = %s AND timestamp = %s",
                (value, device, timestamp))
            cursor.close()
            self.db.commit()
            self.logger.debug("Temperature updated")
    def save_humidity(self, device, timestamp, value):
        self.logger.debug("Saving humidity")
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
        self.logger.debug("Saving wind")
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
        self.logger.debug("saving pressure_readings")
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
        self.logger.debug("saving dewpoint")
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
        self.logger.debug("saving river depth")
        if self.db is None:
            raise FeshieDbError()
        else:
            cursor = self.db.cursor()
            cmd = ("INSERT IGNORE INTO river_depth_readings (device, timestamp,value) VALUES (\"%s\", \"%s\", %s)"% (device, str(timestamp), value))
            self.logger.debug(cmd)
            cursor.execute(cmd)
            cursor.close()
            self.db.commit()

    def save_accelerometer(self, device_id, timestamp, x, y, z):
        self.logger.debug("Saving accelerometer_readings")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO accelerometer_readings (device_id, timestamp,x, y , z) VALUES (%s, %s, %s, %s, %s)",
                (device_id, str(timestamp), x, y, z))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_voltage(self, device_id, timestamp, value):
        self.logger.debug("Saving voltage")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO battery_readings (device_id, timestamp, value) VALUES (%s, %s, %s)",
                (device_id, timestamp, value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)


    def save_mppt(self, device_id, timestamp, value):
        self.logger.debug("Saving MPPT")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO mppt_readings (device_id, timestamp, value) VALUES (%s, %s, %s)",
                (device_id, timestamp, value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_soc(self, device_id, timestamp, value):
        self.logger.debug("Saving SOC")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO soc_readings (device_id, timestamp, value) VALUES (%s, %s, %s)",
                (device_id, timestamp, value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_solar_current(self, device_id, timestamp, value):
        self.logger.debug("Saving solar current")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO solar_current_readings (device_id, timestamp, value) VALUES (%s, %s, %s)",
                (device_id, timestamp, value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_adc(self, device_id, timestamp, adc_id, value):
        self.logger.debug("Saving adc")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO adc_readings (device_id, timestamp, adc_id, value) VALUES (%s, %s, %s, %s)",
                (device_id, str(timestamp), adc_id, value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)


    def save_rain(self, device_id, timestamp, value):
        self.logger.debug("saving rain")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO rain_readings (device_id, timestamp,  value) VALUES (%s, %s, %s)",
                (device_id, str(timestamp), value))
            cursor.close()
            self.db.commit()
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_smart_reading(self, device_id, timestamp, data, processed=False):
        self.logger.debug("saving smart reading")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO unprocessed_smart_data (device_id, timestamp, data, processed) VALUES (%s, %s, %s, %s)",
                (device_id, str(timestamp), data, int(processed)))
            cursor.close()
            self.db.commit()
            self.logger.debug(
                "%s, %s, %d, %s saved into unprocessed_smart_data",
                device_id, timestamp, len(data), processed)
        except MySQLdb.Error as e:
            self.logger.error(e)


    def save_onewire_reading(self, device_id, timestamp, sensor_id, value):
        self.logger.debug("saving one wire")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO onewire_readings (device_id, timestamp, sensor_id, value) VALUES (%s, %s, %s, %s)",
                (device_id, str(timestamp), sensor_id, value))
            cursor.close()
            self.db.commit()
            self.logger.debug(
                "%s, %s, %d, %s saved into onewire_readings",
                device_id, timestamp, sensor_id, value)
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_analog_smart_sensor_reading(self, device_id, timestamp, a1, a2, a3, a4):
        self.logger.debug("saving analog smart sensor")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO analog_smart_sensor_readings (device_id, timestamp, a1, a2, a3, a4) VALUES (%s, %s, %s, %s, %s, %s)",
                (device_id, str(timestamp), a1, a2, a3, a4))
            cursor.close()
            self.db.commit()
            self.logger.debug(
                "%s, %s saved into onewire_readings",
                device_id, timestamp)
        except MySQLdb.Error as e:
            self.logger.error(e)

    def save_chain_reading(
            self, device_id, timestamp, t1, pitch1, roll1,
            t2, pitch2, roll2, t3, pitch3, roll3, t4, pitch4, roll4):
        self.logger.debug("saving chain")
        if self.db is None:
            raise FeshieDbError()
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO chain_readings (device_id, timestamp, t1, pitch1, roll1, t2, pitch2, roll2, t3, pitch3, roll3, t4, pitch4, roll4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (device_id, str(timestamp), t1, pitch1, roll1, t2, pitch2, roll2, t3, pitch3, roll3, t4, pitch4, roll4))
            cursor.close()
            self.db.commit()
            self.logger.debug(
                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s saved into chain_readings",
                device_id, timestamp, t1, pitch1, roll1, 
                t2, pitch2, roll2, t3, pitch3, roll3, 
                t4, pitch4, roll4)
        except MySQLdb.Error as e:
            self.logger.error(e)

    def get_temperature_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\" ), value FROM temperature_readings WHERE device = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_battery_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM battery_readings WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_mppt_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM mppt_readings WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_soc_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM soc_readings WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_solar_current_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM solar_current_readings WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_acceleromter_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT timestamp, pitch, roll FROM accelerometer_converted WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_latest_node_readings(self):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT device, name, timestamp FROM latest_node_readings;")
        return self.db.store_result().fetch_row(0)

    def get_adc_readings(self, node, adc):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\" ), value FROM adc_readings WHERE device_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW() AND adc_id = %s;" %  (node, DATE_LIMIT, adc))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_onewire_ids(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DISTINCT(sensor_id)  FROM `onewire_readings` WHERE `device_id` = \"%s\"" %  node)
        raw = self.db.store_result().fetch_row(0)
        ids = []
        for r in raw:
            ids.append(r[0])
        return ids

    def get_onewire_readings(self, node, sensor_id):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT timestamp, value FROM onewire_readings WHERE device_id = \"%s\" AND sensor_id = \"%s\" AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node, sensor_id, DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_analog_smart_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT timestamp, a1, a2, a3, a4 FROM analog_smart_sensor_readings WHERE device_id = \"%s\"  AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node,  DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw
    
    def get_chain_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT timestamp, t1, pitch1, roll1, t2, pitch2, roll2, t3, pitch3, roll3, t4, pitch4, roll4 FROM chain_readings WHERE device_id = \"%s\"  AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node,  DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_chain_temperatures(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query(
            "SELECT timestamp, ambient, t1, t2, t3, t4 FROM chain_temperatures WHERE device_id = \"%s\";"
            % node)
        return self.db.store_result().fetch_row(0)

    def get_moisture_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM adc_described WHERE device_id = \"%s\"  AND timestamp > \"%s\" AND timestamp <= NOW() AND sensor = \"moisture\";" %  (node,  DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_rain_readings(self, node):
        if self.db is None:
            raise FeshieDbError()
        self.db.query("SELECT DATE_FORMAT( timestamp, \"%%Y-%%m-%%d %%H:%%i:00\"), value FROM rain_hourly WHERE device_id = \"%s\"  AND timestamp > \"%s\" AND timestamp <= NOW();" %  (node,  DATE_LIMIT))
        raw = self.db.store_result().fetch_row(0)
        return raw

    def get_node_name(self, node_id):
        if self.db is None:
            raise FeshieDbError()
        self.db.query(
            "SELECT name FROM current_names WHERE device_id = \"%s\";"
            % node_id)
        try:
            raw = self.db.store_result().fetch_row(0)[0][0]
        except IndexError:
            #Means that there is no known name for this id
            raw = node_id
        return raw

    def get_node_id(self, name):
        if self.db is None:
            raise FeshieDbError()
        self.db.query(
            "SELECT device_id FROM current_names WHERE name = \"%s\";"
            % name)
        try:
            raw = self.db.store_result().fetch_row(0)[0][0]
        except IndexError:
            #Name not known therefore cannot tell what node it is meant to be
            raw = None
        return raw

class FeshieDbConfig(object):
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



class RawReading(object):
    def __init__(self, id, node, recieved_time, data, processed=False):
        self.id = id
        self.node = node
        self.recieved_time = recieved_time
        self.data = data
        self.processed = processed

    def __str__(self):
        return "%s, %s, %s %d, %s" % (self.id, self.node, self.recieved_time, len(self.data), self.processed)

class RawSmartReading(object):
    def __init__(self, id, device, timestamp, data, processed=False):
        self.id = id
        self.device = device
        self.timestamp = timestamp
        self.data = data
        self.processed = processed

    def __str__(self):
        return "%s, %s, %s, %d, %s" % (self.id, self.device, self.timestamp, len(self.data)/2, self.processed)


class ConfigError(Exception):
    """
        An error for when something has gone wrong reading the config
    """
    pass

class FeshieDbError(Exception):
    pass
