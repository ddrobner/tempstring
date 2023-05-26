#!/usr/bin/python

import argparse
import globals

from dateutil import parser as dateparse
from pandas import to_datetime
from pandas import Timestamp

# don't run this if main is imported
if __name__ == "__main__":
    # argparse setup
    parser = argparse.ArgumentParser(
        prog="SNO+ Temperature String Analysis",
        description="Gets temperature string data and spits out plots"
    )

    # self-explanatory
    parser.add_argument('-d', '--date-from')
    parser.add_argument('-D', '--date-to')
    parser.add_argument('--average', help="Plot the average temperature for the given indices", default=None, nargs="+")
    parser.add_argument('--index', help="Plot the temperature for a given index", default=None)
    parser.add_argument('--multiple-index', help="Plot multiple sensors in one plot", default=None, nargs='+')
    parser.add_argument('--cavity-string', action='store_true', help="Plots the cavity string")
    parser.add_argument('--fill-old', nargs="+", help="Fill in missing PSUP data with cavity string data", metavar="FILL_INDICES", default=None)
    parser.add_argument('--heatmap', action='store_true')
    parser.add_argument('--index-offset-start', nargs="+", help="Index shifting start points, for when dealing with the cavity string", default=None)
    parser.add_argument('--index-offset-end', nargs="+", help="Index offset endpoints, for when dealing with the cavity string", default=None)
    parser.add_argument('--debug', action="store_true", help="Enables tools used for debugging the program")

    args = parser.parse_args()

    # setting up global variables
    # TODO clean up setting params since setParam is just a wrapper on dict update - can set all globals in the same call
    globalmanager = globals.globalmanager
    globalmanager.setParam({"date_from": dateparse.parse(args.date_from)})
    globalmanager.setParam({"date_to": dateparse.parse(args.date_to)})
    globalmanager.setParam({"oldstring": args.cavity_string})
    globalmanager.setParam({"tsoffset": Timestamp(year=2023, month=3, day=16)})
    globalmanager.setParam({"debug": args.debug})

    # TODO fix this, this is bad
    # the plotter module importing properly requires the debug flag to be set because of the decorators
    from plotter import Plotting

    try:
        globalmanager.setParam({"fill_old": list(map(int, args.fill_old))})
    except:
        globalmanager.setParam({"fill_old": None})

    try:
        offset_starts = list(map(to_datetime, args.index_offset_start,))
        offset_ends = list(map(to_datetime, args.index_offset_end))
        globalmanager.setParam({"offset_starts": offset_starts})
        globalmanager.setParam({"offset_ends": offset_ends})
    except:
        globalmanager.setParam({"offset_starts": []})
        globalmanager.setParam({"offset_ends": []})

    plotter = Plotting()

    # There should be a better way of doing this but it works fine for the moment
    for k,v in vars(args).items():
        if k == "heatmap" and args.heatmap:
            plotter.histPlot()
        elif k == "average" and args.average != None:
            if len(args.average) > 2:
                indices = list(map(int, args.average))
            else:
                indices = list(range(int(args.average[0]), int(args.average[1])+1))
            plotter.averagePlot(indices)
        elif k == "index" and args.index != None:
            plotter.indexPlot(int(args.index))
        elif k == "multiple_index" and args.multiple_index != None:
            if len(args.multiple_index) > 2:
                indices = list(map(int, args.multiple_index))
            else:
                indices = list(range(int(args.multiple_index[0]), int(args.multiple_index[1]) + 1))
            plotter.compareIndexPlot(indices)
        