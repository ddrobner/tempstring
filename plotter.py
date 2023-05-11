import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import matplotlib.cm as cm
import pandas as pd
import numpy as np

from datetime import datetime
from temperaturestring import TemperatureString

# TODO find out how to uniformly set plot styling separate from each method 
# TODO automatically set ylimit minimum and maximum properly
class Plotting:
    """Module which handles all of the plotting of the data
    """
    def __init__(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to
        self.tempstring = TemperatureString(date_from, date_to)

    def averagePlot(self, indices: list) -> None:
        """Plots the average temperature of a given list of sensor indices

        Args:
            indices (list): List of sensor indices of which to plot the average
        """
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.set_title(f"Average Temperature Measured By Sensors {indices[0]}-{indices[-1]}")
        ax.margins(x=0, y=0.01, tight=True)
        temperaturedata = self.tempstring.indicesMean(indices)
        ax.plot(np.resize(self.tempstring.getTimes(indices[0]).map(lambda x: pd.Timestamp.strftime(x, '%Y-%m-%d %X')).to_numpy(), len(temperaturedata)), temperaturedata, color="black")
        ax.set_ylim(bottom=12, top=13.4)
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
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.set_title(f"Temperature For Sensor {index}")
        ax.margins(x=0, y=0, tight=True)
        ax.plot(self.tempstring.getTimes(index).map(lambda x: pd.Timestamp.strftime(x, "%Y-%m-%d %X")), self.tempstring.getSensorDataByIndex(index)["Temperature"], color="black")
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=15))
        ax.set_ylim(bottom=11)
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Temperature (\u00B0C)")
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/indexPlot_{self.date_from.date()}_{self.date_to.date()}_index[{index}].png", bbox_inches='tight')
    
    def compareIndexPlot(self, indices:list) -> None:
        """Plots multiple sensor indices on the same plot

        Args:
            indices (list): The list of sensor indices to plot
        """
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.margins(x=0, y=0.02, tight=True)
        color = iter(cm.tab20((np.linspace(0, 1, len(indices)))))
        for idx in indices:
            c = next(color)
            temperaturedata = np.resize(self.tempstring.getSensorDataByIndex(idx)["Temperature"].values, len(self.tempstring.getSensorDataByIndex(indices[0])["Temperature"]))
            ax.plot(self.tempstring.getTimes(indices[0]).map(lambda x: pd.Timestamp.strftime(x, "%Y-%m-%d %X")), temperaturedata, label=str(idx), color=c)
        ax.set_title(f"Temperature Data for Sensors {indices[0]}-{indices[-1]}")
        ax.set_ylim(bottom=11.5)
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=15))
        ax.legend(title="Sensor")
        ax.set_xlabel("Date and Time")
        ax.set_ylabel("Temperature (\u00B0C)")
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/compareIndexPlot_{self.date_from.date()}_{self.date_to.date()}_indices[{indices[0]}-{indices[-1]}].png", bbox_inches='tight')
