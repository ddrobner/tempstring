#!/usr/bin/python

import sys

from dbhandler import DatabaseHandler
from sensor import Sensor
from dateutil import parser

dbhandler = DatabaseHandler()


# TODO: improve datetime handling, this is kind of lazy and a bit of a mess
date_from = parser.parse(sys.argv[1])
test_sensor = Sensor(30, dbhandler.getsensor(date_from, 30)) 

print(test_sensor.data)