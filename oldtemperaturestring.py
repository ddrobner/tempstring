from temperaturestring import TemperatureString
from temperaturestring import init_sensor
from dbhandler import DatabaseHandler
from multiprocessing import Pool,cpu_count
from dataprocessing import offset_sensor_indices

import globals
import pandas as pd
import gc

# inherits from TemperatureString
class OldTemperatureString(TemperatureString):
    
    # overriding the constructor here to do old string specific processing
    # going to have default arguments for date from and date to here, since we want this to fill in missing data
    def __init__(self, sensorindices: list, fill: bool=False, date_from: pd.Timestamp=None, date_to: pd.Timestamp=None):
        # pulling in global variables
        self.globalmanager = globals.globalmanager 
        
        # setting up db connection
        dbhandler = DatabaseHandler()

        # creating a mapping of sensor indices (the useful ones) to order in the list
        # faster than finding the sensor index corresponding to the list index every time, and cleaner to write too
        self.sensormap = dict()
        c = 0
        for i in sensorindices:
            self.sensormap.update({i:c})
            c += 1

        # get different data depending upon if filling or not
        if fill:
            sensordata = dbhandler.getall(date_from, date_to, True)
        else:
            sensordata = dbhandler.getall(self.globalmanager.getParam("date_from"), self.globalmanager.getParam("date_to"), True)

        del dbhandler

        df_sensordata = pd.DataFrame(sensordata, columns=["Timestamp", "Sensor Index", "Temperature"])
        df_sensordata["Timestamp"] = df_sensordata["Timestamp"].apply(pd.Timestamp)
        # since the idea is that each sensor should only hold the data for itself I have to do this here, otherwise I'd run it for each sensor which is rather inefficient
        starts = self.globalmanager.getParam("offset_starts")
        print(starts)
        ends = self.globalmanager.getParam("offset_ends")
        print(ends)
        for t in range(len(starts)):
            df_sensordata = offset_sensor_indices(starts[t], ends[t], df_sensordata)

        t_sensordata = (df_sensordata,)*len(sensorindices)
        
        with Pool(maxtasksperchild=1) as p:
            self.sensors = p.starmap(init_sensor, tuple(zip(sensorindices, t_sensordata)))
            p.close()
            p.join()
        del t_sensordata
        del df_sensordata
        gc.collect()

    # everything else here is inherited from TemperatureString
