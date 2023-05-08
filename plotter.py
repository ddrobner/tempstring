from temperaturestring import TemperatureString
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
from datetime import datetime
import pandas as pd

class Plotting:
    def __init__(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to
        self.tempstring = TemperatureString(date_from, date_to)

    def averagePlot(self, indices: list) -> None:
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.tempstring.getTimes().map(lambda x: pd.Timestamp.strftime(x, '%Y-%m-%d %X')), self.tempstring.indicesMean(indices), color="black")
        ax.xaxis.set_major_locator(pltdates.MonthLocator(interval=15))
        plt.gcf().autofmt_xdate()
        fig.savefig(f"plots/indicesMeanPlot_{self.date_from.date()}_{self.date_to.date()}_index[{indices[0]}-{indices[-1]}].png")

