#!/usr/bin/python

import argparse

from dateutil import parser as dateparse
from plotter import Plotting
import globals

# argparse setup
parser = argparse.ArgumentParser(
    prog="PSUP Temperature String Analysis",
    description="Gets PSUP temperature string data and spits out plots"
)

# self-explanatory
parser.add_argument('-d', '--date-from')
parser.add_argument('-D', '--date-to')
parser.add_argument('--average', help="Plot the average temperature for the given indices", default=None, nargs=2, metavar=("INDEX_LOW", "INDEX_HIGH"))
parser.add_argument('--index', help="Plot the temperature for a given index", default=None)
parser.add_argument('--multiple-index', help="Plot multiple sensors in one plot", default=None, nargs=2, metavar=("INDEX_LOW", "INDEX_HIGH"))
parser.add_argument('--old-string', action='store_true', help="Generates plots for the old string")
parser.add_argument('--with-old', action='store_true', help="Overlays the old string over certain plots (lazy implementation at the moment)")

args = parser.parse_args()

globals.oldstring = args.old_string
globals.oldoverlay = args.with_old
globals.date_from = dateparse.parse(args.date_from)
globals.date_to = dateparse.parse(args.date_to)
plotter = Plotting()

# control flow, iterates over the arguments and checks which we passed using a switch
for k, v in vars(args).items():
    match v:
        case None:
            pass
        case args.index:
            plotter.indexPlot(int(args.index))
        case args.multiple_index:
            globals.sensor_min = int(args.multiple_index[0])
            globals.sensor_max = int(args.multiple_index[1])+1
            plotter.compareIndexPlot(list(range(int(args.multiple_index[0]), int(args.multiple_index[1])+1)))
        case args.average:
            globals.sensor_min = int(args.multple_index[0])
            globals.sensor_max = int(args.multiple_index[1]+1)
            plotter.averagePlot(list(range(int(args.average[0]), int(args.average[1])+1)))