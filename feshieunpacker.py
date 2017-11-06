#!/usr/bin/env python

from logging import basicConfig as logging_basicConfig, getLogger, INFO, DEBUG, CRITICAL
from optparse import OptionParser, OptionGroup
from binascii import unhexlify as unhex
from datetime import datetime
from feshiedb import FeshieDb
import protocol_buffers.python.readings_pb2 as readings
import protocol_buffers.python.rs485_message_pb2 as rs485_message
from google.protobuf.message import DecodeError


DEFAULT_LOG_LEVEL = INFO
DEFAULT_CONFIG = "db.ini"


class FeshieUnpacker(object):

    def __init__(self, config, log_level):
        self.logger = getLogger("Feshie unpacker")
        self.logger.setLevel(log_level)
        logging_basicConfig(format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
        self.database = FeshieDb(config, log_level)

    def unpackall(self):
        unprocessed_data = self.database.get_all_unprocessed()
        no_records = len(unprocessed_data)
        self.logger.info("%d Records to process", no_records)
        for record in unprocessed_data:
            node = record.node
            self.logger.info("Processing node %s " % node)
            sample = readings.Sample()
            try:
                sample.ParseFromString(unhex(record.data[2:]))
            except DecodeError as e:
                self.logger.error(
                    "Unpacking %s gave error %s",
                    record.id, e)
                self.database.mark_processed(record.id)
                self.database.mark_corrupt(record.id)
                continue
            timestamp = datetime.utcfromtimestamp(sample.time)
            self.logger.info("Timestamp = %s" % timestamp)
            temperature = sample.temp
            if temperature < -100:
                temperature =  float((((int(temperature *4) ) ^ 0x1FF) +1))/4
            self.database.save_temperature(node, timestamp, temperature)
            power_mode = sample.WhichOneof("battery")
            self.logger.info("Got power mode %s" % power_mode)
            if "power" == power_mode:
                self.logger.info("Unpacking Power board")
                self.database.save_soc(node, timestamp, sample.power.soc)
                self.database.save_mppt(node, timestamp, float(sample.power.mppt)/10)
                self.database.save_solar_current(node, timestamp, float(sample.power.current)/1000)
                self.database.save_voltage(node, timestamp, float(sample.power.batt)/1000)
            elif "batt" == power_mode:
                self.logger.info("Using onboard ADC value for battery reading")
                self.database.save_voltage(node, timestamp, sample.batt)
            else:
                self.logger.warn("No voltage measurement type set (%s)" % node)
            # No longer have the accelerometer so no need to even bother storing data
            #self.database.save_accelerometer(
            #    node, timestamp,
            #    sample.accX, sample.accY, sample.accZ)
            if sample.HasField("ADC1"):
                self.database.save_adc(node, timestamp, 1, sample.ADC1)
            if sample.HasField("ADC2"):
                self.database.save_adc(node, timestamp, 2, sample.ADC2)
            if sample.HasField("rain"):
                self.database.save_rain(node, timestamp, sample.rain)
            if sample.HasField("AVR"):
                self.database.save_smart_reading(node, timestamp, sample.AVR)
            self.database.mark_processed(record.id)
            self.logger.info("Processed %d %s %s", record.id, node, timestamp)

    def unpack_all_smart(self):
        unprocessed_data = self.database.get_all_unprocessed_smart()
        no_records = len(unprocessed_data)
        self.logger.info("%d Smart Records to process", no_records)
        for record in unprocessed_data:
            device = record.device
            timestamp = record.timestamp
            if self.unpack_smart(device, timestamp, record.data) is None:
                self.database.mark_smart_corrupt(record.id)
            self.database.mark_smart_processed(record.id)
            self.logger.info("Processed Smart data %d %s %s", record.id, device, timestamp)



    def unpack_smart(self, device, timestamp, data):
        self.logger.debug("Unpacked %d bytes of smart data", len(data) / 2) #It's hex so each digit is only a nibble
        if len(data) == 0:
            self.logger.error("Length of data = 0, unable to proceed")
            return None
        RS485 = rs485_message.Rs485()
        try:
            RS485.ParseFromString(unhex(data))
        except DecodeError as e:
            self.logger.error("Unpacking buffer gave error %s", e)
            return None
        if RS485.type == rs485_message.Rs485.DATA:
            #this is the type we are expecting
            if RS485.sensor == rs485_message.Rs485.OW:
                self.logger.debug("One wire data")
                for S in RS485.ow:
                    SID = S.id
                    SV = S.value
                    if(248 < SV):          # It should be negative due to bug
                                            # AVR code
                        SV = -float(((int(SV * 16) ^ 0xFFFF)+1))/16
                    self.database.save_onewire_reading(device, timestamp, SID, SV)
                    self.logger.debug("Saved onewire reading to db %s, %s, %s", device, timestamp, SID)
            elif RS485.sensor == rs485_message.Rs485.TA_CHAIN:
                chain = RS485.tad
                self.logger.debug("Chain data")
                self.database.save_chain_reading(
                    device, timestamp, 
                    chain[0].temp, chain[0].pitch, chain[0].roll,
                    chain[1].temp, chain[1].pitch, chain[1].roll,
                    chain[2].temp, chain[2].pitch, chain[2].roll,
                    chain[3].temp, chain[3].pitch, chain[3].roll)
            elif RS485.sensor == rs485_message.Rs485.WP:
                self.logger.debug("WP data")
                if len(RS485.ad) < 2:
                    self.logger.error("Not enough data from waterpressure sensor")
                    return None
                ADC1 = RS485.ad[0].value
                ADC2 = RS485.ad[1].value
                if len(RS485.ad) >=3:
                    ADC3 = RS485.ad[2].value
                    if len(RS485.ad) >= 4:
                        ADC4 = RS485.ad[3].value
                    else:
                        ADC4 = None
                else:
                    ADC3 = None
                    ADC4 = None
                self.database.save_analog_smart_sensor_reading(device, timestamp, ADC1, ADC2, ADC3, ADC4)
                self.logger.debug("Saved analog smart sensor value to db %s %s", device, timestamp)
            else:
                self.logger.error("Unknown sensor type %d", RS485.sensor)
                return None
        else:
            self.logger.error("Unexpected message type %d". RS485.type)
            return None
        return True


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
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG
    else:
        CONFIG = OPTIONS.config_file
    UNPACKER = FeshieUnpacker(CONFIG, LOG_LEVEL)
    UNPACKER.unpackall()
    UNPACKER.unpack_all_smart()
