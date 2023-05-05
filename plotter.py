from temperaturestring import TemperatureString
import matplotlib.pyplot as plt
from datetime import datetime

class Plotting:
    def __init__(self, date_from, date_to):
        self.tempstring = TemperatureString(date_from, date_to)

    def averagePlot(self, indices: list) -> None:
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.tempstring.getTimes().apply(datetime.fromtimestamp), self.tempstring.indicesMean(indices), color="black")
        fig.savefig("plots/testplot.png")

