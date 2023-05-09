#!/usr/bin/python

import argparse

from dateutil import parser as dateparse
from plotter import Plotting

# argparse setup
parser = argparse.ArgumentParser(
    prog="PSUP Temperature String Analysis",
    description="Gets PSUP temperature string data and spits out plots"
)

parser.add_argument('-d', '--date-from')
parser.add_argument('-D', '--date-to')

args = parser.parse_args()

plotter = Plotting(dateparse.parse(args.date_from), dateparse.parse(args.date_to))

#plotter.averagePlot([0, 1, 2, 3, 4, 5, 6])
plotter.indexPlot(0)
