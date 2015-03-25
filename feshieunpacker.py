#!/usr/bin/env python

from logging import basicConfig as logging_basicConfig, getLogger, INFO, DEBUG, CRITICAL
from optparse import OptionParser, OptionGroup
from binascii import unhexlify as unhex
from datetime import datetime
from feshiedb import FeshieDb
import protocol_buffers.readings_pb2 as readings
import protocol_buffers.rs485_message_pb2 as rs485_message
from google.protobuf.message import DecodeError


DEFAULT_LOG_LEVEL = INFO
DEFAULT_CONFIG = "db.ini"
LOGGER = getLogger("Feshie unpacker")
logging_basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def unpackall(config, log_level):
    DATABASE = FeshieDb(config, log_level)
    UNPROCESSED_DATA = DATABASE.get_all_unprocessed()
    NO_RECORDS = len(UNPROCESSED_DATA)
    LOGGER.info("%d Records to process", NO_RECORDS)
    for RECORD in UNPROCESSED_DATA:
        NODE = RECORD.node
        SAMPLE = readings.Sample()
        try:
            SAMPLE.ParseFromString(unhex(RECORD.data[2:]))
        except DecodeError as e:
            LOGGER.error(
                "Unpacking  gave error %s",
                RECORD.id, e)
            DATABASE.mark_processed(RECORD.id)
            DATABASE.mark_corrupt(RECORD.id)
            continue
        TIMESTAMP = datetime.fromtimestamp(SAMPLE.time)
        DATABASE.save_temperature(NODE, TIMESTAMP, SAMPLE.temp)
        DATABASE.save_voltage(NODE, TIMESTAMP, SAMPLE.batt)
        DATABASE.save_accelerometer(
            NODE, TIMESTAMP,
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
        LOGGER.info("Processed %d %s %s", RECORD.id, NODE, TIMESTAMP)

def unpack_all_smart(DATABASE):
    return
    DATABASE.mark_smart_processed(R.id)
    UNPROCESSED_DATA = DATABASE.get_all_unprocessed_smart()
    NO_RECORDS = len(UNPROCESSED_DATA)
    LOGGER.info("%d Smart Records to process", NO_RECORDS)
    for RECORD in UNPROCESSED_DATA:
        DEVICE = RECORD.node
        TIMESTAMP = RECORD.timestamp
        if unpack_smart(DATABASE, DEVICE, TIMESTAMP, DATA) is None:
            DATABASE.mark_smart_corrupt(RECORD.id)
        DATABASE.mark_smart_processed(RECORD.id)
        LOGGER.info("Processed Smart data %d %s %s", RECORD.id, NODE, TIMESTAMP)



def unpack_smart(DATABASE, DEVICE, TIMESTAMP, DATA):
    LOGGER.debug("Unpacked %d bytes of smart data", len(DATA) / 2) #It's hex so each digit is only a nibble
    RS485 = rs485_message.Rs485()
    try:
        RS485.ParseFromString(unhex(DATA))
    except DecodeError as e:
        LOGGER.error("Unpacking buffer gave error %s", e)
        return None
    if RS485.type == rs485_message.Rs485.DATA:
        #this is the type we are expecting
        if RS485.sensor == rs485_message.Rs485.OW:
            LOGGER.debug("One wire data")
            for S in RS485.ow:
                SID = S.id
                SV = S.value
                DATABASE.save_onewire_reading(DEVICE, TIMESTAMP, SID, SV)
                LOGGER.debug("Saved onewire reading to db %s, %s, %s", DEVICE, TIMESTAMP, SID)
        elif RS485.sensor == rs485_message.Rs485.TA_CHAIN:
            for C in RS485.tad:
                LOGGER.debug("Chain data")
                #DATABASE.save_chain_reading(DEVICE, TIMESTAMP)
        elif RS485.sensor == rs485_message.Rs485.WP:
            LOGGER.debug("WP data")
            if len(RS485.ad) < 2:
                LOGGER.error("Not enough data from waterpressure sensor")
                return None
            ADC1 = RS485.ad[0]
            ADC2 = RS485.ad[1]
            if len(RS485.ad) >=3:
                ADC3 = RS485.ad[2]
                if len(RS485.ad) >= 4:
                    ADC4 = RS485.ad[3]
                else:
                    ADC4 = None
            else:
                ADC3 = None
            DATABASE.save_analog_smart_sensor_reading(self, DEVICE, TIMESTAMP, ADC1, ADC2, ADC3, ADC4)
            LOGGER.debug("Saved analog smart sensor value to db %s %s", DEVICE, TIMESTAMP)
        else:
            LOGGER.error("Unknown sensor type %d", RS485.sensor)
            return None
    else:
        LOGGER.error("Unexpected message type %d". RS485.type)
        return None


if __name__ == "__main__":
    LOG_LEVEL = DEFAULT_LOG_LEVEL
    PARSER = OptionParser()
    GROUP = OptionGroup(
        PARSER, "Verbosity Options",
        "Options to change the level of output")
    GROUP.add_option(
        "-q", "--quiet", action="store_true",
        dest="quiet", default=False,
        help="Supress all but critical errors")
    GROUP.add_option(
        "-v", "--verbose", action="store_true",
        dest="verbose", default=False,
        help="Print all information available")
    PARSER.add_option_group(GROUP)
    PARSER.add_option(
        "-c", "--config", action="store",
        type="string", dest="config_file",
        help="Config file containing database credentials")
    (OPTIONS, ARGS) = PARSER.parse_args()
    if OPTIONS.quiet:
        LOG_LEVEL = CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = DEBUG
    LOGGER.setLevel(LOG_LEVEL)
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG
    else:
        CONFIG = OPTIONS.config_file
    unpackall(CONFIG, LOG_LEVEL)
