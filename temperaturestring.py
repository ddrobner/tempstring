from sensor import Sensor
from dbhandler import DatabaseHandler

import pandas as pd
import gc
import numpy as np
import globals

from multiprocessing import Pool

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
    def __init__(self, sensorindices: list=list(range(0, 28))) -> None:
        """Constructor for TemperatureString

        Args:
            start_date (datetime.date): Data start date
            end_date (datetime.date): Data end date
        """
        databasehandler = DatabaseHandler()

        self.globalmanager = globals.globalmanager
        # index the sensors sequentiall internally to make iteration easier
        # since if we only handle, say sensors 7-12 then indexing breaks
        self.sensormap = dict()
        c = 0 
        for i in sensorindices:
            self.sensormap.update({i:c})
            c += 1

        # first sensor index for the new PSUP string in the database is 30
        sensor_offset = 30

        sensordata = databasehandler.getall(self.globalmanager.getParam("date_from"), self.globalmanager.getParam("date_to"))
        # getting rid of database handler once we get the data
        del databasehandler
        df_sensordata =  pd.DataFrame(sensordata, columns=["Timestamp", "Sensor Index", "Temperature"])
        df_sensordata["Sensor Index"] = df_sensordata["Sensor Index"].apply(lambda x: x-sensor_offset) 

        t_sensordata = (df_sensordata,)*len(sensorindices)

        # storing each sensor object in a list
        with Pool(maxtasksperchild=1) as p:
            self.sensors = p.starmap(init_sensor, tuple(zip(sensorindices, t_sensordata)))
            p.close()
            p.join()
        del t_sensordata
        gc.collect()


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
        cur_data = self.sensors[self.sensormap[indices[0]]].data["Temperature"].to_numpy(copy=True)
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
