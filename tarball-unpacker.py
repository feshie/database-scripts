#! /usr/bin/env python
# unpack the feshie tar ball and extract parts
from shutil import move, rmtree
from os import listdir, stat,remove
from os.path import exists, isdir
from datetime import datetime
import tarfile
from subprocess import Popen
import sys
from sys import argv
import logging
# Where we unpack
UNPACKED="/home/mountainsensing/www/feshie/unpacked/"
WEBCAM="/home/mountainsensing/www/feshie/webcams/estate/"
LOGFILES="/home/mountainsensing/www/feshie/logfiles/"
ARCHIVE="/home/mountainsensing/www/feshie/archive/"

def extract_file(filename):
    tf = tarfile.open(name=filename, mode="r")
    tf.extractall(UNPACKED)
    tf.close


def process_image(filename):
    logging.debug("processing: %s" %filename)
    new_fname = WEBCAM + filename.split("/")[-1].split("_")[2]+".jpg"
    _move(filename, new_fname)

def _move(src, dst):
    if not exists(dst):
        move(src,dst)
        logging.debug("file moved to %s " % dst)
    else:
        logging.warn("File %s already exists" % dst)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    if len(argv) != 2:
        logging.critical("Must specify filename to extract")
        exit(1)
    tarball = argv[1]
    try:
        logging.info("unpacking")
        extract_file(tarball)
    except IOError as e:
        logging.critical("Failed to unpack tarball")
        exit(3)
    l = listdir(UNPACKED + "/data")
    if l == []:
        logging.critical("No files unpacked")
        exit(4)
    for f in l:
        if "TIMING" in f:
            process_image(UNPACKED + "/data/" + f )
        if f == "python-log" or f == "executable_output":
            #Stub files don't contain anything useful
            remove("%sdata/%s" % (UNPACKED,f))
            logging.info("%s removed" % f)
            continue
        if "log" in f or "output" in f:
            _move("%sdata/%s" % (UNPACKED,f) ,LOGFILES + f)
    _move(tarball, ARCHIVE + tarball.split("/")[-1]) 
