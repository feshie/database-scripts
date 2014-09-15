import logging
import protocol_buffers.readings_pb2 as readings
from math import atan2, sqrt, pi, pow

def printReading(reading):
    print ("Time: %s" % reading.time)
    print ("Temp: %i" % reading.temp)
    print("Batv: %i" % reading.batt)
    pitch, roll = convert_accel(
        reading.accX, reading.accY, reading.accZ)
    print("Accel: %.2f,%.2f"% (round(pitch,2), round(roll,2)))
    if reading.HasField("ADC1"):
        print("ADC1: %i" % reading.ADC1)
    if reading.HasField("ADC2"):
        print("ADC2: %i" % reading.ADC2)
    if reading.HasField("rain"):
        print("Rain: %i" % reading.rain)
    if reading.HasField("AVR"):
        print("Have %i bytes of AVR data" % len(reading.AVR))


def convert_accel(x, y, z):
    pitch = atan2(y, z) * 180 / pi
    roll = atan2(x, sqrt(pow(y,2) + pow(z,2))) * 180 / pi
    return (pitch, roll)
