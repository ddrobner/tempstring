import pandas as pd
from datetime import datetime 

class Sensor:
    def __init__(self, index:int, temperaturedata):
        self.idx = index
        self.tempdata =  pd.DataFrame(temperaturedata, columns=["Timestamp", "Sensor Index", "Temperature"])
        # going to convert timestamps to unix timestamps here
        self.tempdata["Timestamp"] = self.tempdata["Timestamp"].apply(datetime.timestamp)
    
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

    
