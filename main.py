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
parser.add_argument('--average', help="Plot the average temperature for the given indices", default=None, nargs=2, metavar=("INDEX_LOW", "INDEX_HIGH"))
parser.add_argument('--index', help="Plot the temperature for a given index", default=None)
parser.add_argument('--multiple-index', help="Plot multiple sensors in one plot", default=None, nargs=2, metavar=("INDEX_LOW", "INDEX_HIGH"))

args = parser.parse_args()

plotter = Plotting(dateparse.parse(args.date_from), dateparse.parse(args.date_to))

for k, v in vars(args).items():
    match v:
        case None:
            pass
        case args.index:
            plotter.indexPlot(int(args.index))
        case args.multiple_index:
            plotter.compareIndexPlot(list(range(int(args.multiple_index[0]), int(args.multiple_index[1])+1)))
        case args.average:
            plotter.averagePlot(list(range(int(args.average[0]), int(args.average[1])+1)))