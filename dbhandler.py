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

        # 
        self.cur = self.db_conn.cursor()

    def getall(self, date:datetime.date):
        self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp > '{date.year}-{date.month}-{date.day}') AND (sensor >= 30) AND (sensor <= 56) ORDER BY timestamp")
        fetched_data = self.cur.fetchall()
        return fetched_data

    def getsensor(self, date:datetime.date, sensoridx:int):
        self.cur.execute(f"SELECT * FROM public.cavity_temp WHERE (timestamp > '{date.year}-{date.month}-{date.day}') AND (sensor = {sensoridx}) ORDER BY timestamp")
        return self.cur.fetchall()
