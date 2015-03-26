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

    def get_temperature_readings(self):
        nodes = self.get_nodes()
        self.logger.info("Using nodes %s", nodes)
        header = ["timestamp"]
        header.extend(nodes)
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
