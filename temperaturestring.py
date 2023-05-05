from sensor import Sensor
from dbhandler import DatabaseHandler
from copy import copy
import pandas as pd
import numpy as np

class TemperatureString:
    def __init__(self, start_date, end_date):
        databasehandler = DatabaseHandler()
        # setting the minimum and maximum sensor ranges
        sensor_min = 0
        sensor_max = 25
        # first sensor index for the new PSUP string in the database is 30
        sensor_offset = 30
        # storing each sensor object in a list
        self.sensors = []
        for s in range(sensor_min, sensor_max+1):
            sensor_data = databasehandler.getsensor(start_date, s+sensor_offset)
            self.sensors.append(Sensor(s, sensor_data))

    def getSensorDataByIndex(self, index:int) -> pd.DataFrame:
        return self.sensors[index].data

    def getStringData(self) -> list:
        return [s.data for s in self.sensors]

    # computes the mean temperature for given indices over whatever period of time we are looking at
    def indicesMean(self, indices:list) -> np.ndarray:
        cur_data = copy(self.sensors[indices[0]].data)
        for idx in indices[1:]:
            cur_data +=  self.sensors[idx].data
        return cur_data["Temperature"]/len(cur_data["Temperature"])

    def getTimes(self):
        return self.sensors[0].data["Timestamp"]
