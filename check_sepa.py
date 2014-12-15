#!/usr/bin/env python

from feshiedb import FeshieDb
import logging
from optparse import OptionParser, OptionGroup

DEFAULT_LOG_LEVEL = logging.ERROR
DEFAULT_CONFIG = "/home/pjb/database-scripts/db.ini"

WARN_THRESHOLD = 1080
CRITICAL_THRESHOLD = 1440


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
    logger = logging.getLogger("Latest unpacker")
    logger.setLevel(LOG_LEVEL)
    DB = FeshieDb(CONFIG)
    DIFF = -1
    DIFF = DB.get_sepa_difference()
    if DIFF > CRITICAL_THRESHOLD:
        print("CRITICAL: No data for more than %d minutes" %
            CRITICAL_THRESHOLD)
        exit(2)
    elif DIFF > WARN_THRESHOLD:
        print("WARNING: No data for more than %d minutes" %
            WARN_THRESHOLD)
        exit(1)
    elif DIFF >= 0:
        print("OK: Latest data is %d minutes old" % DIFF)
        exit(0)
    else:
        print("UNKNOWN: Unable to get difference")
        exit(3)

