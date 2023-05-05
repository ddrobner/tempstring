from temperaturestring import TemperatureString
import matplotlib.pyplot as plt
from datetime import datetime

class Plotting:
    def __init__(self, date_from: datetime.date, date_to: datetime.date):
        self.date_from = date_from
        self.date_to = date_to
        self.tempstring = TemperatureString(date_from, date_to)

    def averagePlot(self, indices: list) -> None:
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.tempstring.getTimes().apply(datetime.fromtimestamp), self.tempstring.indicesMean(indices), color="black")
        fig.savefig(f"plots/indicesMeanPlot_{self.date_from.date()}_{self.date_to.date()}_idx{indices[0]}-{indices[-1]}.png")

