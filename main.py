#!/usr/bin/python

import argparse
import globals

from dateutil import parser as dateparse
from plotter import Plotting
from pandas import Timestamp

# argparse setup
parser = argparse.ArgumentParser(
    prog="PSUP Temperature String Analysis",
    description="Gets PSUP temperature string data and spits out plots"
)

# self-explanatory
parser.add_argument('-d', '--date-from')
parser.add_argument('-D', '--date-to')
parser.add_argument('--average', help="Plot the average temperature for the given indices", default=None, nargs="+", metavar=("INDEX_LOW", "INDEX_HIGH"))
parser.add_argument('--index', help="Plot the temperature for a given index", default=None)
parser.add_argument('--multiple-index', help="Plot multiple sensors in one plot", default=None, nargs='+', metavar=("INDEX_LOW", "INDEX_HIGH"))
parser.add_argument('--old-string', action='store_true')
parser.add_argument('--fill-old', nargs="+", help="Fill in missing data with old string data", metavar="FILL_INDICES", default=None)

args = parser.parse_args()

# setting up global variables
# TODO clean up setting params since setParam is just a wrapper on dict update - can set all globals in the same call
globalmanager = globals.globalmanager
globalmanager.setParam({"date_from": dateparse.parse(args.date_from)})
globalmanager.setParam({"date_to": dateparse.parse(args.date_to)})
globalmanager.setParam({"oldstring": args.old_string})
globalmanager.setParam({"tsoffset": Timestamp(year=2023, month=3, day=16)})

try:
    globalmanager.setParam({"fill_old": list(map(int, args.fill_old))})
except:
    globalmanager.setParam({"fill_old": None})

plotter = Plotting()

# control flow, iterates over the arguments and checks which we passed using a switch
for k, v in vars(args).items():
    match v:
        case None:
            pass
        case args.index:
            plotter.indexPlot(int(args.index))
        case args.multiple_index:
            if len(args.multiple_index) > 2:
                indices = list(map(int, args.multiple_index))
            else:
                indices = list(range(int(args.multiple_index[0]), int(args.multiple_index[1]) + 1))
            plotter.compareIndexPlot(indices)
        case args.average:
            if len(args.average) > 2:
                indices = list(map(int, args.average))
            else:
                indices = list(range(int(args.average[0]), int(args.average[1])+1))
            plotter.averagePlot(indices)
