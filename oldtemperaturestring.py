from temperaturestring import TemperatureString
from temperaturestring import init_sensor
from dbhandler import DatabaseHandler
from multiprocessing import Pool,cpu_count
from dataprocessing import offset_sensor_indices

import globals
import pandas as pd

# inherits from TemperatureString
class OldTemperatureString(TemperatureString):
    
    # overriding the constructor here to do old string specific processing
    # going to have default arguments for date from and date to here, since we want this to fill in missing data
    def __init__(self, sensorindices: list, date_from: pd.Timestamp=globals.globalmanager.getParam("date_from"), date_to: pd.Timestamp=globals.globalmanager.getParam("date_to")):
        # pulling in global variables
        self.globalmanager = globals.globalmanager 
        
        # setting up db connection
        dbhandler = DatabaseHandler()

        self.sensormap = dict()
        c = 0
        for i in sensorindices:
            self.sensormap.update({i:c})
        
        sensordata = dbhandler.getall(date_from, date_to, True)
        df_sensordata = pd.DataFrame(sensordata, columns=["Timestamp", "Sensor Index", "Temperature"])
        df_sensordata["Timestamp"] = df_sensordata["Timestamp"].apply(pd.Timestamp)
        # since the idea is that each sensor should only hold the data for itself I have to do this here, otherwise I'd run it for each sensor which is rather inefficient
        df_sensordata = offset_sensor_indices(self.globalmanager.getParam("tsoffset"), df_sensordata)

        t_sensordata = (df_sensordata,)*len(sensorindices)
        
        with Pool(cpu_count()) as p:
            self.sensors = p.starmap(init_sensor, tuple(zip(sensorindices, t_sensordata)))

    # everything else here is inherited from TemperatureString
