import pandas as pd
from datetime import datetime 

from dataprocessing import fill_blank_timestamps

class Sensor:
    def __init__(self, index:int, temperaturedata):
        self.idx = index
        self.tempdata =  pd.DataFrame(temperaturedata, columns=["Timestamp", "Sensor Index", "Temperature"])
        # pandas has a timestamp column type, which will make it rather easy to fill missing timestamps
        self.tempdata["Timestamp"] = self.tempdata["Timestamp"].apply(pd.Timestamp)
        self.tempdata = fill_blank_timestamps(self.tempdata)
        self.tempdata["Sensor Index"] = self.tempdata["Sensor Index"].apply(lambda x: x-30)

    
    # getter method for whatever data the sensor has
    # plan to do something cooler in the future but right now just want to get things working
    @property
    def data(self):
        return self.tempdata

    # property for the index of the sensor on the string
    # may be useful
    @property
    def index(self):
        return self.idx

    
