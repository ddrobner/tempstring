#!/usr/bin/python

import argparse

from dateutil import parser as dateparse
from temperaturestring import TemperatureString

# argparse setup
parser = argparse.ArgumentParser(
    prog="PSUP Temperature String Analysis",
    description="Gets PSUP temperature string data and spits out plots"
)

parser.add_argument('-d', '--date-from')
parser.add_argument('-D', '--date-to')

args = parser.parse_args()

# the none is a placeholder since at the moment using the end date is not implemented
tmpstring = TemperatureString(dateparse.parse(args.date_from), None)

print(tmpstring.getSensorDataByIndex(1))