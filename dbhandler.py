import os
from psycopg2 import connect
import datetime

class DatabaseHandler:
    """Handles interactions with the database
    """
    def __init__(self):
        """Constructor for DatabaseHandler
        """

        # database information from Mark
        # note - must be on SL-SNOLAB vpn to access
        self.dbname = "detector"
        self.dbaddress = "192.168.80.120"

        # getting database username and password from environment variables
        self.dbusername = os.environ.get("SNODBUSER")
        self.dbpass = os.environ.get("SNODBPASS")

        # db connection
        self.db_conn = connect(dbname=self.dbname, host=self.dbaddress, user=self.dbusername, password=self.dbpass)

        # autocommitting changes - should probably get rid of at some point
        self.db_conn.autocommit=True

        # need to declare this but we don't do any funny stuff with the cursor
        self.cur = self.db_conn.cursor()

    # gets the data for all sensors from the database
    def getall(self, date_from: datetime.date, date_to: datetime.date, new_string: bool=False) -> list:
        """Fetches all data from the database in a given time

        Args:
            date_from (datetime.date): Starting date for data
            date_to (datetime.date): Ending date for data

        Returns:
            list: List containing the fetched data from the SQL server
        """
        match new_string:
            case False:
                self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp >= '{date_from.year}-{date_from.month}-{date_from.day}') AND (timestamp <= '{date_to.year}-{date_to.month}-{date_to.day}') AND (sensor >= 30) AND (sensor <= 56) ORDER BY timestamp")
            case True:
                self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp >= '{date_from.year}-{date_from.month}-{date_from.day}') AND (timestamp <= '{date_to.year}-{date_to.month}-{date_to.day}') AND (sensor >= 0) AND (sensor <= 29) ORDER BY timestamp")
        return self.cur.fetchall() 

    # gets the data for a specific sensor from the database
    def getsensor(self, date_from:datetime.date, date_to: datetime.date, sensoridx:int) -> list:
        """Fetches data for a specific sensor from the database for a given timeframe

        Args:
            date_from (datetime.date): Starting date for data
            date_to (datetime.date): Ending date for data
            sensoridx (int): Index of temperature sensor from 0 to 27 TODO verify this

        Returns:
            list: Fetched data for the sensor
        """
        self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp >= '{date_from.year}-{date_from.month}-{date_from.day}') AND (timestamp <= '{date_to.year}-{date_to.month}-{date_to.day}') AND (sensor = {sensoridx}) ORDER BY timestamp")
        return self.cur.fetchall()
