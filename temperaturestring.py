from sensor import Sensor
from dbhandler import DatabaseHandler

import pandas as pd
import numpy as np
import datetime
import globals

from multiprocessing import Pool
from multiprocessing import cpu_count

def init_sensor(index: int, sensordata:pd.DataFrame) -> Sensor:
    """Helper function to initialize a Sensor, for use with multiprocessing Pool

    Args:
        index (int): Sensor index 
        sensordata (pd.DataFrame): Sensor data 

    Returns:
        Sensor: The initialized sensor object 
    """
    return Sensor(index, sensordata)


class TemperatureString:
    """An object encapsulating all of the sensors, to make interfacing with any number of them easier
    """
    def __init__(self) -> None:
        """Constructor for TemperatureString

        Args:
            start_date (datetime.date): Data start date
            end_date (datetime.date): Data end date
        """
        databasehandler = DatabaseHandler()
        # setting the minimum and maximum sensor ranges

        self.sensormap = dict() 
        sensor_range = list(range(globals.sensor_min, globals.sensor_max+1))
        for i in range(0, (globals.sensor_max - globals.sensor_min)+1):
            self.sensormap.update({sensor_range[i]:i})

        # first sensor index for the new PSUP string in the database is 30
        sensor_offset = 30 if not globals.oldstring else 0

        sensordata = databasehandler.getall(globals.date_from, globals.date_to)
        df_sensordata =  pd.DataFrame(sensordata, columns=["Timestamp", "Sensor Index", "Temperature"])
        df_sensordata["Sensor Index"] = df_sensordata["Sensor Index"].apply(lambda x: x-sensor_offset) 

        t_sensordata = (df_sensordata,)*(globals.sensor_max + (1 - globals.sensor_min))
        t_sensorids = tuple(range(globals.sensor_min, globals.sensor_max+1))

        # storing each sensor object in a list
        with Pool(cpu_count()) as p:
            self.sensors = p.starmap(init_sensor, tuple(zip(t_sensorids, t_sensordata)))


    def getSensorDataByIndex(self, index:int) -> pd.DataFrame:
        """Gets sensor data for a specific sensor index

        Args:
            index (int): Sensor index

        Returns:
            pd.DataFrame: Dataframe containing the sensor data
        """
        return self.sensors[self.sensormap[index]].data

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
        cur_data = self.sensors[0].data["Temperature"].to_numpy(copy=True)
        for idx in indices[1:]:
            cur_data += np.resize(self.sensors[self.sensormap[idx]].data["Temperature"].to_numpy(), len(cur_data))
        # TODO figure out a better way to fill in the blank timestamps, have to do this again so as to not include zero-elements in averaging
        return np.divide(cur_data,len(indices))

    def getTimes(self, index: int) -> pd.Series:
        """Gets the time data for a sensor

        Args:
            index (int): Sensor index

        Returns:
            pd.Series: A series containing time data for the sensor
        """
        return self.sensors[self.sensormap[index]].data["Timestamp"]
