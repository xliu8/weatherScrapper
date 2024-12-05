"""
Author: Mandeep Kaur
Assistant: Xiahoan Liu, Doahn Chung
Created: 2024-11-01
Updated: 2024-11-07

Weather Data Scraper for Environment Canada
=========================================

This module provides functionality to scrape and process historical weather data
from Environment Canada's climate data website. It specifically targets the daily
temperature records, handling various data formats and missing values.

Features:
---------
- Scrapes daily maximum, minimum, and mean temperatures
- Handles missing or accumulated data markers ('M' and 'A')
- Validates and processes temperature values
- Supports negative and positive temperature values
- Traverses through historical data month by month

Usage:
------
Basic usage example:
```python
scraper = WeatherScraper()
weather_data = scraper.scrape_weather_data()
print(weather_data)
```

Data Format:
-----------
The scraped data is returned as a dictionary with the following structure:
{
    'YYYY-MM-DD': {
        'Max': float,  # Maximum temperature
        'Min': float,  # Minimum temperature
        'Mean': float  # Mean temperature
    }
}

Temperature Processing Rules:
--------------------------
1. Valid temperatures: Both positive and negative numeric values
2. Invalid markers: 'M' (missing) and 'A' (accumulated)
3. Processing logic:
   - All temperatures invalid: Record is skipped
   - Some temperatures valid: Invalid values are set to 0
   - Missing mean: Calculated as (max + min) / 2 if available
   - Valid temperatures are converted to float values
"""

from datetime import datetime
import urllib.request
from html.parser import HTMLParser
import json
import os

class WeatherScraper(HTMLParser):
    """
    A custom HTML parser for scraping weather data from Environment Canada's website.

    This class extends HTMLParser to navigate through the HTML structure of the
    weather data pages and extract daily temperature records. It handles data
    validation, processing, and storage of temperature values.

    Attributes:
        weather_data (dict): Stores processed weather data indexed by date
        daily_temps (dict): Temporary storage for processing daily records
        current_date (str): Current date being processed
        current_year (int): Year being processed
        current_month (int): Month being processed
        prev_month_exists (bool): Flag indicating if previous month data exists

    State Tracking Attributes:
        in_tbody (bool): Currently parsing table body
        in_tr (bool): Currently parsing table row
        in_abbr (bool): Currently parsing abbreviation
        in_td (bool): Currently parsing table cell
        column (int): Current column index in row
    """

    def __init__(self):
        """Initialize the WeatherScraper with default values and state trackers."""
        super().__init__()
        self.in_tbody = False
        self.in_tr = False
        self.in_abbr = False
        self.in_td = False
        self.column = 0
        self.current_date = None
        self.daily_temps = {}
        self.weather_data = {}
        self.current_year = None
        self.current_month = None
        self.output_file = 'weather_data.json'

    def handle_starttag(self, tag, attrs):
        """
        Process opening HTML tags to track position in document structure.

        Args:
            tag (str): HTML tag name
            attrs (list): List of (attribute, value) pairs
        """
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.column = 0
        elif tag == "abbr" and self.in_tr:
            self.in_abbr = True
        elif tag == "td" and self.in_tr and self.column < 3:
            self.in_td = True


    def handle_endtag(self, tag):
        """
        Process closing HTML tags and trigger data processing when appropriate.

        Args:
            tag (str): HTML tag name
        """
        if tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            self.in_tr = False
            if self.current_date and self.daily_temps:
                self._process_daily_temps()
            self.current_date = None
            self.daily_temps = {}
        elif tag == "abbr":
            self.in_abbr = False
        elif tag == "td":
            self.in_td = False
            self.column += 1

    def _is_valid_temp(self, temp):
        """
        Check if a temperature value is valid (numeric, possibly negative).

        Args:
            temp (str): Temperature value to validate

        Returns:
            bool: True if temperature is valid numeric value, False otherwise
        """
        try:
            float(temp)
            return True
        except ValueError:
            return False

    def _process_daily_temps(self):
        """
        Process and validate daily temperature records.

        Handles various cases:
        - All temperatures valid: Store as floats
        - Some temperatures valid: Replace invalid with 0
        - All temperatures invalid: Skip record
        - Missing mean: Calculate from max and min if possible
        """
        if not all(key in self.daily_temps for key in ["Max", "Min", "Mean"]):
            return

        max_temp = self.daily_temps["Max"]
        min_temp = self.daily_temps["Min"]
        mean_temp = self.daily_temps["Mean"]

        # Count valid temperatures - True => 1, false => 0
        valid_temps = sum(1 for temp in [max_temp, min_temp, mean_temp]
                         if self._is_valid_temp(temp))

        if valid_temps == 0:
            return

        if valid_temps < 3:
            processed_temps = {}
            processed_temps["Max"] = float(max_temp) if self._is_valid_temp(max_temp) else 0
            processed_temps["Min"] = float(min_temp) if self._is_valid_temp(min_temp) else 0

            if self._is_valid_temp(mean_temp):
                processed_temps["Mean"] = float(mean_temp)
            else:
                processed_temps["Mean"] = (processed_temps["Max"] + processed_temps["Min"]) / 2

            self.weather_data[self.current_date] = processed_temps
        else:
            self.weather_data[self.current_date] = {
                "Max": float(max_temp),
                "Min": float(min_temp),
                "Mean": float(mean_temp)
            }

    def handle_data(self, data):
        """
        Process text content within HTML tags.

        Args:
            data (str): Text content from HTML document
        """
        data = data.strip()
        try:
            if (self.in_abbr) and data.isdigit():
                day = int(data)
                self.current_date = datetime(self.current_year, self.current_month, day).strftime('%Y-%m-%d')
            elif self.in_td and self.current_date:
                if self.column == 0:
                    self.daily_temps["Max"] = data
                elif self.column == 1:
                    self.daily_temps["Min"] = data
                elif self.column == 2:
                    self.daily_temps["Mean"] = data
        except ValueError:
            print(f"Error processing data: {data}")

    def fetch_data_for_month(self, year, month):
        """
        Fetch weather data for a specific month and year.

        Args:
            year (int): Year to fetch data for
            month (int): Month to fetch data for

        Returns:
            bool: True if previous month exists, False otherwise
        """
        self.current_year = year
        self.current_month = month
        print(month)
        url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}"

        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
            self.feed(html)
        except Exception as e:
            print(f"Error fetching data for {year}-{month:02d}: {e}")

    def scrape_weather_data(self):
        """
        Scrape weather data starting from current month and going backwards.

        Returns:
            dict: Dictionary of processed weather data indexed by date
        """
        today = datetime.today()
        year, month = 2020, 1
        while (year <= today.year):
            self.fetch_data_for_month(year, month)

            month += 1

            if month == 13:
                month = 1
                year += 1
        return self.weather_data
    
    def fetch_weather_data(self):
        try:
            if not os.path.exists(self.output_file):
                with open(self.output_file, 'w') as file:
                    json.dump(self.scrape_weather_data(), file, indent=4)

            with open(self.output_file, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: The file {self.output_file} was not found.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.output_file}.")
        except Exception as e:
            print(f"Error: An Exception occurred - {e}")



if __name__ == "__main__":
    scraper = WeatherScraper()
    print(scraper.fetch_weather_data())