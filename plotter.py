import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import matplotlib.cm as cm
import pandas as pd
import numpy as np

from temperaturestring import TemperatureString
from oldtemperaturestring import OldTemperatureString
from multiprocessing import Pool
from multiprocessing import cpu_count
from copy import copy
import globals

# TODO fix autolimits on averageplot - will be more work than you expect 
class Plotting:
    """Module which handles all of the plotting of the data
    """
    def __init__(self):
        # pull in our global variables
        self.globalmanager = globals.globalmanager
        self.date_from = self.globalmanager.getParam("date_from") 
        self.date_to = self.globalmanager.getParam("date_to")

        # declare figure and axes in the constructor to unify formatting
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        # formatting options common to all plots
        plt.rcParams['font.size'] = 18
        self.ax.grid()
        self.ax.margins(x=0, y=0.01, tight=True)
        # changing formatting depending on plot range
        fmt = pltdates.DateFormatter('%b') if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.DateFormatter("%Y-%m-%d")
        self.ax.xaxis.set_major_formatter(fmt)
        # and using mpl's auto date locators
        self.ax.xaxis.set_major_locator(pltdates.MonthLocator() if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.AutoDateLocator())
        self.ax.xaxis.set_minor_locator(pltdates.DayLocator())
        self.ax.tick_params(axis="both", which="major", labelsize=14)
        self.ax.set_xlabel("Date and Time", fontsize=18)
        self.ax.set_ylabel("Temperature (\u00B0C)", fontsize=18)
        # need to declare the legend after plotting, so just going to create a dict of legend kwargs and unzip it
        self.legendparams = {'loc':'center left', 'bbox_to_anchor':(1, 0.5), 'title':'Sensor'} 
        plt.gcf().autofmt_xdate()



    def averagePlot(self, indices: list) -> None:
        """Plots the average temperature of a given list of sensor indices

        Args:
            indices (list): List of sensor indices of which to plot the average
        """
        indices.sort()
        self.tempstring = TemperatureString(indices) if not self.globalmanager.getParam("oldstring") else OldTemperatureString(indices)

        # getting and plotting the data
        temperaturedata = self.tempstring.indicesMean(indices)
        times = self.tempstring.getTimes(indices[0]).to_numpy()
        self.ax.plot(np.resize(times, len(temperaturedata)), temperaturedata, color="black", label="New String")

        if self.globalmanager.getParam("fill_old") != None:
            overlay_indices = copy(self.globalmanager.getParam("fill_old"))
            overlay_indices.sort()
            self.old_overlay_plot(overlay_indices)
            self.ax.set_title(f"Average Temperature Measured By Sensors {indices[0]}-{indices[-1]} With Old String Average of Sensors {', '.join(str(s) for s in overlay_indices)}")
            self.ax.legend(**self.legendparams)
        else:
            self.ax.set_title(f"Average Temperature Measured By Sensors {f'{indices[0]}-{indices[-1]}' if not self.globalmanager.getParam('oldstring') else ', '.join(str(i) for i in indices) + ' on the Old String'}", label="New String")


        # autoformatting here is pretty wacky
        # splitting this out because it's going to be a long one
        # the sensors don't stop reporting at the exact same timestamp so we have some weird low values here
        # going to get the argmin and shift it by some amount to take a point where they're all actual data
        # that was the plan at least, will have to come back to this
        # I concede on this one, going to eventually add a plotoptions argument to set the limits
        self.ax.set_ylim(bottom=11, top=(temperaturedata.max() + 0.1))
        self.fig.savefig(f"plots/meanPlot_{self.date_from.date()}_{self.date_to.date()}_index[{indices[0]}-{indices[-1]}]{'_oldstring' if self.globalmanager.getParam('oldstring') else ''}{'_fill_old' if self.globalmanager.getParam('fill_old') != None else ''}.png", bbox_inches='tight')

    def indexPlot(self, index: int) -> None:
        """Plots the temperature data for a specific sensor

        Args:
            index (int): Index of the sensor to plot
        """
        self.tempstring = TemperatureString([index]) if not self.globalmanager.getParam("oldstring") else OldTemperatureString([index])
        self.ax.set_title(f"Temperature For Sensor {index} {'on the Old String' if self.globalmanager.getParam('oldstring') else ''}")
        self.ax.margins(x=0, y=0, tight=True)
        plotdata = self.tempstring.getSensorDataByIndex(index)["Temperature"]
        self.ax.plot(self.tempstring.getTimes(index), plotdata, color="black")
        self.ax.set_ylim(bottom=plotdata[plotdata != 0].min()-0.1, top=plotdata.max()+0.1)
        self.ax.legend(**self.legendparams)
        self.fig.savefig(f"plots/indexPlot_{self.date_from.date()}_{self.date_to.date()}_index[{index}]{'_oldstring' if self.globalmanager.getParam('oldstring') else ''}.png", bbox_inches='tight')
    
    def compareIndexPlot(self, indices:list) -> None:
        """Plots multiple sensor indices on the same plot

        Args:
            indices (list): The list of sensor indices to plot
        """
        # initializing things
        indices.sort()
        self.tempstring = TemperatureString(indices) if not self.globalmanager.getParam("oldstring") else OldTemperatureString(indices)
        # initializing these as infinities so the first iteration is always the current min/max
        # very much a math person thing to do lol
        absmin = np.Inf
        absmax = -1*np.Inf
        # tuples of arguments to zip together for starmap
        l_sensordata = [self.tempstring.getSensorDataByIndex(k)["Temperature"].values for k in indices]
        l_reshapelength = (len(self.tempstring.getSensorDataByIndex(indices[0])["Temperature"]),)*len(l_sensordata)
        # multithread array reshaping since it was slow
        with Pool(cpu_count()) as p:
            shaped_data = p.starmap(np.resize, zip(l_sensordata, l_reshapelength))
        for d in shaped_data:
            cmin = d[d != 0].min()
            cmax = d.max()
            absmin = cmin if (cmin < absmin) else absmin
            absmax = cmax if (cmax > absmax) else absmax
        # use mpl colormaps to assign a different color to each line automatically 
        color = iter(cm.tab20((np.linspace(0, 1, len(indices)))))
        for idx in range(len(shaped_data)):
            c = next(color)
            self.ax.plot(self.tempstring.getTimes(indices[0]), shaped_data[idx], label=str(indices[idx]), color=c)
        # change title depending on if using the old or new string
        if self.globalmanager.getParam("oldstring"):
            self.ax.set_title(f"Temperature Data for Sensors {', '.join(str(i) for i in indices)} on the Old String")
        else:
            self.ax.set_title(f"Temperature Data for Sensors {indices[0]}-{indices[-1]}")
        # using the min and max from before to autoset the ylimits
        self.ax.set_ylim(bottom=(absmin - 0.1), top=(absmax + 0.1))
        self.ax.legend(**self.legendparams)
        self.fig.savefig(f"plots/multipleIndexPlot_{self.date_from.date()}_{self.date_to.date()}_indices[{indices[0]}-{indices[-1]}]{'_oldstring' if self.globalmanager.getParam('oldstring') else ''}.png", bbox_inches='tight')

    def old_overlay_plot(self, indices):
        old_tmpstring = OldTemperatureString(indices)
        oldplot_data = old_tmpstring.indicesMean(indices)
        self.ax.plot(np.resize(old_tmpstring.getTimes(indices[0]).to_numpy(), len(oldplot_data)), oldplot_data, color="red", label="Old String", alpha=0.75)
