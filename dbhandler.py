import os
from psycopg2 import connect
import datetime

class DatabaseHandler:
    def __init__(self):
        # database information from Mark
        # note - must be on SL-SNOLAB vpn to access
        self.dbname = "detector"
        self.dbaddress = "192.168.80.120"

        # getting database username and password from environment variables
        self.dbusername = os.environ.get("SNODBUSER")
        self.dbpass = os.environ.get("SNODBPASS")

        self.db_conn = connect(dbname=self.dbname, host=self.dbaddress, user=self.dbusername, password=self.dbpass)

        # autocommitting changes - should probably get rid of at some point
        self.db_conn.autocommit=True

        self.cur = self.db_conn.cursor()

    # gets the data for all sensors from the database
    def getall(self, date_from: datetime.date, date_to: datetime.date):
        self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp > '{date_from.year}-{date_from.month}-{date_from.day}') AND (timestamp < '{date_to.year}-{date_to.month}-{date_to.day}') AND (sensor >= 30) AND (sensor <= 56) ORDER BY timestamp")
        fetched_data = self.cur.fetchall()
        return fetched_data

    # gets the data for a specific sensor from the database
    def getsensor(self, date_from:datetime.date, date_to: datetime.date, sensoridx:int):
        self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp > '{date_from.year}-{date_from.month}-{date_from.day}') AND (timestamp < '{date_to.year}-{date_to.month}-{date_to.day}') AND (sensor = {sensoridx}) ORDER BY timestamp")
        return self.cur.fetchall()
