from sensor import Sensor
from dbhandler import DatabaseHandler

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
        for s in range(sensor_min, sensor_max):
            sensor_data = databasehandler.getsensor(start_date, s+sensor_offset)
            self.sensors.append(Sensor(s, sensor_data))

    def getSensorDataByIndex(self, index:int):
        return self.sensors[index].data
