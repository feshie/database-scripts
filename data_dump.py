from logging import basicConfig as logging_basicConfig, getLogger, WARN
from datetime import datetime

from feshiedb import FeshieDb

class DataDump(object):

    def __init__(self, config, log_level=WARN):
        self.logger = getLogger("Data dump")
        self.logger.setLevel(log_level)
        logging_basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.database = FeshieDb(config, log_level)


    def get_nodes(self):
        return self.database.get_z1_nodes()

    def get_latest_readings(self):
        return self.database.get_latest_node_readings()

    def get_temperature_readings(self):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        for node in nodes:
            header.append(self.database.get_node_name(node))
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for node in nodes:
            self.logger.debug("Processing node %s", node)
            values = self.database.get_temperature_readings(node)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, node, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, nodes)
        self.logger.debug("%d timestamps in sorted data", len(sorted_data))
        data.extend(sorted_data)
        return data

    def get_battery_readings(self):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        for node in nodes:
            header.append(self.database.get_node_name(node))
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for node in nodes:
            self.logger.debug("Processing node %s", node)
            values = self.database.get_battery_readings(node)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, node, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, nodes)
        self.logger.debug("%d timestamps in sorted data", len(sorted_data))
        data.extend(sorted_data)
        return data

    def get_adc_readings(self, adc):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        for node in nodes:
            header.append(self.database.get_node_name(node))
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for node in nodes:
            self.logger.debug("Processing node %s", node)
            values = self.database.get_adc_readings(node, adc)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, node, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, nodes)
        self.logger.debug("%d timestamps in sorted data", len(sorted_data))
        data.extend(sorted_data)
        return data

    def get_moisture_readings(self):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        for node in nodes:
            header.append(self.database.get_node_name(node))
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for node in nodes:
            self.logger.debug("Processing node %s", node)
            values = self.database.get_moisture_readings(node)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, node, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, nodes)
        self.logger.debug("%d timestamps in sorted data", len(sorted_data))
        data.extend(sorted_data)
        return data

    def get_rain_readings(self):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        for node in nodes:
            header.append(self.database.get_node_name(node))
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for node in nodes:
            self.logger.debug("Processing node %s", node)
            values = self.database.get_rain_readings(node)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, node, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, nodes)
        self.logger.debug("%d timestamps in sorted data", len(sorted_data))
        data.extend(sorted_data)
        return data

    def get_accelerometer_readings(self, node):
        raw = self.database.get_acceleromter_readings(node)
        data = [["timestamp", "pitch", "roll"]]
        for r in raw:
            line = [r[0], r[1], r[2]]
            data.append(line)
        return data

    def get_onewire_readings(self, node):
        ids = self.database.get_onewire_ids(node)
        self.logger.info("Using node %s ids %s ", node, ids)
        header = ["timestamp"]
        header.extend(ids)
        data = [header]
        data_raw = {}
        self.logger.debug(data)
        for i in ids:
            self.logger.debug("Processing id %s", ids)
            values = self.database.get_onewire_readings(node, i)
            self.logger.debug("Got %d readings", len(values))
            for value in values:
                data_raw = merge_data(data_raw, i, value)
        self.logger.info("%d timestamps in data", len(data_raw))
        sorted_data = sort_data(data_raw, ids)
        data.extend(sorted_data)
        return data

    def get_analog_smart_readings(self, node):
        raw = self.database.get_analog_smart_readings(node)
        header = ["timestamp", "ADC1", "ADC2", "ADC3", "ADC4"]
        data = [header]
        for i in raw:
            data.append([i[0], i[1], i[2], i[3], i[4]])
        return data

    def get_chain_readings(self, node):
        raw = self.database.get_chain_readings(node)
        header = [
            "timestamp", 
            "Temp 1", "Pitch 1", "Roll 1",
            "Temp 2", "Pitch 2", "Roll 2",
            "Temp 3", "Pitch 3", "Roll 3",
            "Temp 4", "Pitch 4", "Roll 4"]
        data = [header]
        for i in raw:
            data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12]])
        return data

    def get_chain_temperature_readings(self, node):
        raw = self.database.get_chain_temperatures(node)
        header = [
            "timestamp", "Ambient", "t1", "t2", "t3", "t4"]
        data = [header]
        for i in raw:
            data.append([i[0], i[1], i[2], i[3], i[4], i[5]])
        return data

def merge_data(output, node, values):
    timestamp = values[0]
    value = values[1]
    if not timestamp in output.keys():
        #not a previously seen timestamp
        output[timestamp] = {}
    output[timestamp][node] = value
    return output

def sort_data(data_raw, nodes):
    timestamps = sorted(data_raw.keys())
    data = []
    for t in timestamps:
        a = []
        a.append(t)
        for s in nodes:
            try:
                a.append(data_raw[t][s])
            except KeyError:
                a.append(None)
        data.append(a)
    return data 

def csv_convert(data):
    output = ""
    for line in data:
        for cell in line:
            print cell
            if cell is not None:
                output+= "%s," % cell
            else:
                output+=","
        output += ("\n")
    return output
