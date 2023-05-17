import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import matplotlib.cm as cm
import pandas as pd
import numpy as np

from datetime import datetime
from temperaturestring import TemperatureString
from multiprocessing import Pool
from multiprocessing import cpu_count
from matplotlib.ticker import AutoMinorLocator
import globals

# TODO find out how to uniformly set plot styling separate from each method 
# TODO automatically set ylimit minimum and maximum properly
class Plotting:
    """Module which handles all of the plotting of the data
    """
    def __init__(self):
        self.globalmanager = globals.globalmanager
        self.date_from = self.globalmanager.getParam("date_from") 
        self.date_to = self.globalmanager.getParam("date_to")
        self.font = {'family' : 'sans',
        'weight' : 'bold',
        'size'   : 20}
        self.params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}


    def averagePlot(self, indices: list) -> None:
        """Plots the average temperature of a given list of sensor indices

        Args:
            indices (list): List of sensor indices of which to plot the average
        """
        self.tempstring = TemperatureString(self.date_to, min(indices), max(indices))
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set_title(f"Average Temperature Measured By Sensors {indices[0]}-{indices[-1]}")
        ax.margins(x=0, y=0.01, tight=True)
        #plt.rc('font', **self.font)
        #plt.rcParams.update(self.params)
        plt.rcParams['font.size'] = 18
        temperaturedata = self.tempstring.indicesMean(indices)
        # autoformatting here is pretty wacky
        # splitting this out because it's going to be a long one
        # the sensors don't stop reporting at the exact same timestamp so we have some weird low values here
        # going to get the argmin and shift it by some amount to take a point where they're all actual data
        # that was the plan at least, will have to come back to this
        # I concede on this one, going to eventually add a plotoptions argument to set the limits
        ax.set_ylim(bottom=12.2, top=(temperaturedata.max() + 0.1))
        ax.plot(np.resize(self.tempstring.getTimes(indices[0]).to_numpy(), len(temperaturedata)), temperaturedata, color="black")
        ax.xaxis.set_major_locator(pltdates.MonthLocator(bymonthday=3))
        ax.xaxis.set_major_formatter(pltdates.DateFormatter("%b"))
        #ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.xaxis.set_minor_locator(pltdates.DayLocator(interval=7))
        ax.grid()
        plt.gcf().autofmt_xdate()
        ax.set_xlabel("Date and Time", fontsize=18)
        ax.set_ylabel("Temperature (\u00B0C)", fontsize=18)
        fig.savefig(f"plots/meanPlot_{self.date_from.date()}_{self.date_to.date()}_index[{indices[0]}-{indices[-1]}].png", bbox_inches='tight')

    def indexPlot(self, index: int) -> None:
        """Plots the temperature data for a specific sensor

        Args:
            index (int): Index of the sensor to plot
        """
        self.tempstring = TemperatureString(index, index)
        fig, ax = plt.subplots(figsize=(20, 10))
        #plt.rc('font', **self.font)
        #plt.rcParams.update(self.params)
        plt.rcParams['font.size'] = 18
        ax.set_title(f"Temperature For Sensor {index} {'on the Old String' if self.globalmanager.getParam('oldstring') else ''}")
        ax.margins(x=0, y=0, tight=True)
        plotdata = self.tempstring.getSensorDataByIndex(index)["Temperature"]
        ax.plot(self.tempstring.getTimes(index), plotdata, color="black")
        ax.set_ylim(bottom=plotdata[plotdata != 0].min()-0.1, top=plotdata.max()+0.1)
        fmt = pltdates.DateFormatter('%b') if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(pltdates.MonthLocator() if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.AutoDateLocator())
        ax.xaxis.set_minor_locator(pltdates.DayLocator())
        ax.set_xlabel("Date", fontsize=18)
        ax.set_ylabel("Temperature (\u00B0C)", fontsize=18)
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/indexPlot_{self.date_from.date()}_{self.date_to.date()}_index[{index}]{'_oldstring' if self.globalmanager.getParam('oldstring') else ''}.png", bbox_inches='tight')
    
    def compareIndexPlot(self, indices:list) -> None:
        """Plots multiple sensor indices on the same plot

        Args:
            indices (list): The list of sensor indices to plot
        """
        self.tempstring = TemperatureString(min(indices), max(indices))
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.grid()
        plt.rcParams['font.size'] = 18
        ax.margins(x=0, y=0.02, tight=True)
        color = iter(cm.tab20((np.linspace(0, 1, len(indices)))))
        # initializing these as infinities so the first iteration is always the current min/max
        # very much a math person thing to do lol
        absmin = np.Inf
        absmax = -1*np.Inf
        l_sensordata = [self.tempstring.getSensorDataByIndex(k)["Temperature"].values for k in indices]
        l_reshapelength = (len(self.tempstring.getSensorDataByIndex(indices[0])["Temperature"]),)*len(l_sensordata)
        with Pool(cpu_count()) as p:
            shaped_data = p.starmap(np.resize, zip(l_sensordata, l_reshapelength))
        for d in shaped_data:
            cmin = d[d != 0].min()
            cmax = d.max()
            absmin = cmin if (cmin < absmin) else absmin
            absmax = cmax if (cmax > absmax) else absmax
        monthdisplay = True if (self.date_to - self.date_from) > pd.Timedelta(6, "m") else False
        for idx in range(len(shaped_data)):
            c = next(color)
            ax.plot(self.tempstring.getTimes(indices[0]), shaped_data[idx], label=str(indices[idx]), color=c)
        if self.globalmanager.getParam("oldstring"):
            ax.set_title(f"Temperature Data for Sensors {indices} on the Old String")
        else:
            ax.set_title(f"Temperature Data for Sensors {indices[0]}-{indices[-1]}")
        ax.set_ylim(bottom=(absmin - 0.1), top=(absmax + 0.1))
        fmt = pltdates.DateFormatter('%b') if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(pltdates.MonthLocator() if (self.date_from - self.date_to) > pd.Timedelta(3, "m") else pltdates.AutoDateLocator())
        ax.xaxis.set_minor_locator(pltdates.DayLocator())
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Sensor")
        ax.tick_params(axis="both", which="major", labelsize=14)
        ax.set_xlabel("Date and Time", fontsize=18)
        ax.set_ylabel("Temperature (\u00B0C)", fontsize=18)
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/multipleIndexPlot_{self.date_from.date()}_{self.date_to.date()}_indices[{indices[0]}-{indices[-1]}]{'_oldstring' if self.globalmanager.getParam('oldstring') else ''}.png", bbox_inches='tight')
