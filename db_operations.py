"""
Description: 
Author: Doanh Chung
Assistant: Xiaohan Liu, Mandeep Kaur
Date: 2024 - 11 - 11
Usage: Initialize the database and Create the table.
"""
import sqlite3
import scrape_weather
from dbcm import DBCM

class DBOperations:
    def __init__(self):
        try:
            with DBCM("weather.sqlite") as cursor:
                self.initialize_db(cursor)
            print("Opened database successfully.")
        except Exception as e:
            print(f"An Error Has Occurred During Opening Database: {e}")

    def initialize_db(self, cursor):
        """
        Initializes the database. If there is no WeatherData table, it will be created.
        """
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='WeatherData';")
            table_exists = cursor.fetchone() is not None

            if table_exists:
                print(f"The table WeatherData exists.")
            else:
                print(f"The table WeatherData does not exist.")
                cursor.execute("""create table WeatherData
                                (id integer primary key autoincrement not null,
                                sample_date text not null,
                                location text not null,
                                min_temp real not null,
                                max_temp real not null,
                                avg_temp real not null,
                                unique(sample_date, location));""")
                
                print("Table created successfully.")
        except Exception as e:
            print(f"An Error Has Occurred During Creation Of Table: {e}")

    def insert_to_table(self, dictionary):
        """
        Insert data into table.
        """
        try:
            sql = """insert or ignore into WeatherData (sample_date,location,min_temp,max_temp,avg_temp)
                    values (?,?,?,?,?)"""
            with DBCM("weather.sqlite") as cursor:
                for date, data in dictionary.items():
                    data = (date, 'Winnipeg, MB', data['Min'], data['Max'], data['Mean'])
                    cursor.execute(sql, data)
                    
            print("Added sample successfully.")
        except Exception as e:
            print(f"An Error Has Occurred During Insertion Into Table: {e}")

    def fetch_data(self):
        """
        Fetch the data used for plotting.

        Returns:
            plotting_data: Dictionary of a month's daily mean temperatures indexed by the month.
        """
        plotting_data = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        try:
            with DBCM("weather.sqlite") as cursor:
                for row in cursor.execute("select * from WeatherData"):
                    plotting_data[int(row[1][5:7])].append(row[5])
            print(plotting_data)
            return plotting_data
        except Exception as e:
            print(f"An Error Has Occurred During Fetching Of Data: {e}")

    def save_data(self):
        """
        Save data to the database.

        """
        fetched_data = self.fetch_data()
        print(f"Save data - {fetched_data}")
        scraper = scrape_weather.WeatherScraper()
        self.insert_to_table(scraper.fetch_weather_data())

    def purge_data(self):
        """
        Deletes all data in the database.
        """
        try:
            with DBCM("weather.sqlite") as cursor:
                cursor.execute("delete from WeatherData")
            print("Data has been purged.")
        except Exception as e:
            print(f"An Error Has Occurred During Data Purging: {e}")

            
weather_table = DBOperations()
# print(weather_table.fetch_data())
weather_table.save_data()
# weather_table.purge_data()
weather_table.fetch_data()