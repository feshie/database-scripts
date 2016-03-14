#!/usr/bin/env python

from feshiedb import FeshieDb
import sys

def correct(value):
    if value < -100 :
        return float((((int(value *4) ) ^ 0x1FF) +1))/4
    else:
        return value


def correct_values(node, db):
    readings = db.get_temperature_readings(node)
    for reading in readings:
        timestamp = reading[0]
        old_value = reading[1]
        if ( old_value >= -100):
            continue
        else:
            new_value = correct(old_value)
            print "Corrected %f to %f at reading %s" % ( old_value, new_value, timestamp)
            db.update_temperature(node, timestamp, new_value)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        node = sys.argv[1]
        db = FeshieDb("db.ini")
        if not node in db.get_z1_nodes():
            print "Not a valid node"
        else:
            print "Node ID ok"
            correct_values(node, db)
    else:
        print "Usage: %s <node_id>" % sys.argv[0]
    


