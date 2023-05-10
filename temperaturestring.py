from sensor import Sensor
from dbhandler import DatabaseHandler
from copy import copy
from functools import reduce
import pandas as pd
import numpy as np
import datetime

class TemperatureString:
    """An object encapsulating all of the sensors, to make interfacing with any number of them easier
    """
    def __init__(self, start_date:datetime.date, end_date: datetime.date) -> None:
        """Constructor for TemperatureString

        Args:
            start_date (datetime.date): Data start date
            end_date (datetime.date): Data end date
        """
        databasehandler = DatabaseHandler()
        # setting the minimum and maximum sensor ranges
        sensor_min = 0
        sensor_max = 25
        # first sensor index for the new PSUP string in the database is 30
        sensor_offset = 30
        # storing each sensor object in a list
        self.sensors = []
        for s in range(sensor_min, sensor_max+1):
            sensor_data = databasehandler.getsensor(start_date, end_date, s+sensor_offset)
            self.sensors.append(Sensor(s, sensor_data))

    def getSensorDataByIndex(self, index:int) -> pd.DataFrame:
        """Gets sensor data for a specific sensor index

        Args:
            index (int): Sensor index

        Returns:
            pd.DataFrame: Dataframe containing the sensor data
        """
        return self.sensors[index].data

    def getStringData(self) -> list:
        """Gets data for the whole TemperatureString

        Returns:
            list: List of DataFrames with the data for each sensor
        """
        return [s.data for s in self.sensors]

    # computes the mean temperature for given indices over whatever period of time we are looking at
    def indicesMean(self, indices:list) -> np.ndarray:
        """Computes the mean temperature for the list of given sensors as an array

        Args:
            indices (list): The indices to compute the mean of

        Returns:
            np.ndarray: Array containing mean temperature at each time
        """
        cur_data = copy(self.sensors[0].data["Temperature"]).to_numpy()
        for idx in indices[1:]:
            cur_data += np.resize(self.sensors[idx].data["Temperature"].to_numpy(), len(cur_data))
        return cur_data/len(indices)

    def getTimes(self, index: int) -> pd.Series:
        """Gets the time data for a sensor

        Args:
            index (int): Sensor index

        Returns:
            pd.Series: A series containing time data for the sensor
        """
        return self.sensors[index].data["Timestamp"]
