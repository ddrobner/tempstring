import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import matplotlib.cm as cm
import pandas as pd
import numpy as np

from datetime import datetime
from temperaturestring import TemperatureString
from multiprocessing import Pool
from multiprocessing import cpu_count

# TODO find out how to uniformly set plot styling separate from each method 
# TODO automatically set ylimit minimum and maximum properly
class Plotting:
    """Module which handles all of the plotting of the data
    """
    def __init__(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to

    def averagePlot(self, indices: list) -> None:
        """Plots the average temperature of a given list of sensor indices

        Args:
            indices (list): List of sensor indices of which to plot the average
        """
        self.tempstring = TemperatureString(self.date_from, self.date_to, min(indices), max(indices))
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.set_title(f"Average Temperature Measured By Sensors {indices[0]}-{indices[-1]}")
        ax.margins(x=0, y=0.01, tight=True)
        temperaturedata = self.tempstring.indicesMean(indices)
        # autoformatting here is pretty wacky
        # splitting this out because it's going to be a long one
        # the sensors don't stop reporting at the exact same timestamp so we have some weird low values here
        # going to get the argmin and shift it by some amount to take a point where they're all actual data
        # that was the plan at least, will have to come back to this
        # I concede on this one, going to eventually add a plotoptions argument to set the limits
        ax.set_ylim(bottom=11.5, top=(temperaturedata.max() + 0.1))
        ax.plot(np.resize(self.tempstring.getTimes(indices[0]).map(lambda x: pd.Timestamp.strftime(x, '%Y-%m-%d %X')).to_numpy(), len(temperaturedata)), temperaturedata, color="black")
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=25))
        plt.gcf().autofmt_xdate()
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Temperature (\u00B0C)")
        fig.savefig(f"plots/indicesMeanPlot_{self.date_from.date()}_{self.date_to.date()}_index[{indices[0]}-{indices[-1]}].png", bbox_inches='tight')

    def indexPlot(self, index: int) -> None:
        """Plots the temperature data for a specific sensor

        Args:
            index (int): Index of the sensor to plot
        """
        self.tempstring = TemperatureString(self.date_from, self.date_to, index, index)
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.set_title(f"Temperature For Sensor {index}")
        ax.margins(x=0, y=0, tight=True)
        plotdata = self.tempstring.getSensorDataByIndex(index)["Temperature"]
        ax.plot(self.tempstring.getTimes(index).map(lambda x: pd.Timestamp.strftime(x, "%Y-%m-%d %X")), plotdata, color="black")
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=15))
        ax.set_ylim(bottom=plotdata[plotdata != 0].min()-0.1, top=plotdata.max()+0.1)
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Temperature (\u00B0C)")
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/indexPlot_{self.date_from.date()}_{self.date_to.date()}_index[{index}].png", bbox_inches='tight')
    
    def compareIndexPlot(self, indices:list) -> None:
        """Plots multiple sensor indices on the same plot

        Args:
            indices (list): The list of sensor indices to plot
        """
        self.tempstring = TemperatureString(self.date_from, self.date_to, min(indices), max(indices))
        fig, ax = plt.subplots(figsize=(20, 10))
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
        for idx in range(len(shaped_data)):
            c = next(color)
            ax.plot(self.tempstring.getTimes(indices[0]).map(lambda x: pd.Timestamp.strftime(x, "%Y-%m-%d %X")), shaped_data[idx], label=str(idx), color=c)
        ax.set_title(f"Temperature Data for Sensors {indices[0]}-{indices[-1]}")
        ax.set_ylim(bottom=(absmin - 0.1), top=(absmax + 0.1))
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=15))
        ax.legend(title="Sensor")
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Temperature (\u00B0C)")
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/compareIndexPlot_{self.date_from.date()}_{self.date_to.date()}_indices[{indices[0]}-{indices[-1]}].png", bbox_inches='tight')
