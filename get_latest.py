#!/usr/bin/env python

from feshiedb import FeshieDb
import logging
import protocol_buffers.readings_pb2 as readings
from feshie_reading import printReading
from optparse import OptionParser, OptionGroup
#from google.protobuf.message import DecodeError
from binascii import unhexlify as unhex

DEFAULT_LOG_LEVEL = logging.ERROR
DEFAULT_CONFIG = "db.ini"

def unpacklatest(DB_CONFIG, LOG_LEVEL):
    logger = logging.getLogger("Latest unpacker")
    logger.setLevel(LOG_LEVEL)
    DB = FeshieDb(DB_CONFIG)
    RAW = DB.get_latest_unprocessed()
    SAMPLE = readings.Sample()
    print "node: %s" % RAW.node
    print "Recieved time: %s" % RAW.recieved_time
    print "Processed: %s" % RAW.processed
    print "Raw data:%s" % RAW.data
    #try:
    SAMPLE.ParseFromString(unhex(RAW.data[2:]))
    #except DecodeError:
     #   print("Unable to decode protocol buffer")
      #  return
    printReading(SAMPLE)


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
        LOG_LEVEL = logging.CRITICAL
    elif OPTIONS.verbose:
        LOG_LEVEL = logging.DEBUG
    if OPTIONS.config_file is None:
        CONFIG = DEFAULT_CONFIG
    else:
        CONFIG = OPTIONS.config_file
    unpacklatest(CONFIG, LOG_LEVEL)
