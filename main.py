#!/usr/bin/python

import sys

from dbhandler import DatabaseHandler
import datetime
from dateutil import parser

dbhandler = DatabaseHandler()


# TODO: improve datetime handling, this is kind of lazy and a bit of a mess
date_from = parser.parse(sys.argv[1])
# testing database access
print(dbhandler.getsensor(date_from, 30))
