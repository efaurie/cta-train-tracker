import csv
import urllib
import os.path
import sqlite3


class StationDataAccessor():

    def __init__(self):
        if os.path.isfile('cta_info.db'):
            self.connection = sqlite3.connect('cta_info.db')
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect('cta_info.db')
            self.cursor = self.connection.cursor()
            self.init_data()

    def init_data(self):
        cta_system_csv = urllib.urlretrieve('https://data.cityofchicago.org/api/views/8pix-ypme/rows.csv?accessType=DOWNLOAD')
        cta_system_info = open(cta_system_csv[0], 'rb')
        input_data = csv.reader(cta_system_info)
        header = next(input_data, None)

        self.init_table(header)

        for row in input_data:
            row = map(lambda x: x.replace("'", ''), row)
            row = map(lambda x: "'" + x + "'", row)
            fields = ', '.join(row)
            command = "INSERT INTO CTA VALUES({0})".format(fields)
            self.cursor.execute(command)

        self.connection.commit()

    def init_table(self, header):
        header = map(lambda x: x + " TEXT", header)
        columns = ', '.join(header)
        command = 'CREATE TABLE CTA({0})'.format(columns)
        self.cursor.execute(command)
        self.connection.commit()

    def get_station_name_by_id(self, stop_id):
        command = 'SELECT STATION_NAME FROM CTA WHERE STOP_ID = {0}'.format(stop_id)
        self.cursor.execute(command)
        return self.extract_first_result()

    def get_description_by_id(self, stop_id):
        query = 'SELECT STATION_DESCRIPTIVE_NAME FROM CTA WHERE STOP_ID = {0}'.format(stop_id)
        self.cursor.execute(query)
        return self.extract_first_result()

    def get_stop_id_from_station_and_direction(self, station_name, direction):
        query = 'SELECT STOP_ID FROM CTA WHERE STATION_NAME = {0} AND DIRECTION_ID = {1}'.format(station_name, direction)
        self.cursor.execute(query)
        return self.extract_first_result()

    def extract_first_result(self):
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]