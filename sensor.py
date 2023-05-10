import pandas as pd
from datetime import datetime 

from dataprocessing import fill_blank_timestamps

class Sensor:
    """Object which stores the data for a single sensor, don't use outside of the TemperatureString class
    """
    def __init__(self, index:int, temperaturedata:pd.DataFrame):
        """Constructor for Sensor

        Args:
            index (int): Sensor index which we are initializing
            temperaturedata (pd.DataFrame): DataFrame containing the sensor data
        """
        self.idx = index
        self.tempdata =  pd.DataFrame(temperaturedata, columns=["Timestamp", "Sensor Index", "Temperature"])
        # pandas has a timestamp column type, which will make it rather easy to fill missing timestamps
        self.tempdata["Timestamp"] = self.tempdata["Timestamp"].apply(pd.Timestamp)
        self.tempdata = fill_blank_timestamps(self.tempdata)
        self.tempdata["Sensor Index"] = self.tempdata["Sensor Index"].apply(lambda x: x-30)

    
    # getter method for whatever data the sensor has
    # plan to do something cooler in the future but right now just want to get things working
    @property
    def data(self) -> pd.DataFrame:
        """Getter method for the sensor data

        Returns:
            pd.DataFrame: The sensor data
        """
        return self.tempdata

    # property for the index of the sensor on the string
    # may be useful
    @property
    def index(self) -> int:
        """Getter method for sensor index

        Returns:
            int: Sensor index
        """
        return self.idx

    
