#!/usr/bin/env python

from logging import basicConfig as logging_basicConfig, getLogger, INFO, ERROR, DEBUG, CRITICAL
from optparse import OptionParser, OptionGroup
from binascii import unhexlify as unhex
from datetime import datetime
from feshiedb import FeshieDb
import protocol_buffers.readings_pb2 as readings
from google.protobuf.message import DecodeError


DEFAULT_LOG_LEVEL = INFO
DEFAULT_CONFIG = "db.ini"


def unpackall(config, log_level):
    LOGGER = getLogger("Feshie unpacker")
    LOGGER.setLevel(LOG_LEVEL)
    logging_basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    DATABASE = FeshieDb(config, log_level)
    UNPROCESSED_DATA = DATABASE.get_all_unprocessed()
    NO_RECORDS = len(UNPROCESSED_DATA)
    LOGGER.info("%d Records to process" % NO_RECORDS)
    for RECORD in UNPROCESSED_DATA:
        NODE = RECORD.node
        SAMPLE = readings.Sample()
        try:
            SAMPLE.ParseFromString(unhex(RECORD.data[2:]))
        except DecodeError as e:
            LOGGER.error("Unpacking %s gave error %s" 
                % (RECORD.id, e))
            continue
        TIMESTAMP = datetime.fromtimestamp(SAMPLE.time)
        DATABASE.save_temperature(NODE, TIMESTAMP, SAMPLE.temp)
        DATABASE.save_voltage(NODE, TIMESTAMP, SAMPLE.batt)
        DATABASE.save_accelerometer(NODE, TIMESTAMP,
            SAMPLE.accX, SAMPLE.accY, SAMPLE.accZ)
        if SAMPLE.HasField("ADC1"):
            DATABASE.save_adc(NODE, TIMESTAMP, 1, SAMPLE.ADC1)
        if SAMPLE.HasField("ADC2"):
            DATABASE.save_adc(NODE, TIMESTAMP, 2, SAMPLE.ADC2)
        if SAMPLE.HasField("rain"):
            DATABASE.save_rain(NODE, TIMESTAMP, SAMPLE.rain)
        if SAMPLE.HasField("AVR"):
            DATABASE.save_smart_reading(NODE, TIMESTAMP, SAMPLE.AVR)
        DATABASE.mark_processed(RECORD.id)
        LOGGER.info("Processed %d %s %s" %(RECORD.id, NODE, TIMESTAMP))
        



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
        LOG_LEVEL = CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = DEBUG
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG
    else:
        CONFIG = OPTIONS.config_file
    unpackall(CONFIG, LOG_LEVEL)
