import matplotlib.pyplot as plt
import json
from collections import defaultdict

class PlotOperations:
    def __init__(self, weather_data):
        """
        Initializes with weather data from JSON format, grouped by month and year.
        :param weather_data: Dictionary where keys are dates and values contain "Mean" temperatures.
        """
        self.weather_data = self._parse_weather_data(weather_data)

    def _parse_weather_data(self, weather_data):
        """
        Parses the JSON data to organize mean temperatures by month and year.
        :param weather_data: JSON data with dates as keys and temperature details as values.
        :return: Dictionary with years as keys, each containing a dictionary with months as keys
                 and lists of mean daily temperatures as values.
        """
        monthly_data = defaultdict(lambda: defaultdict(list))
        
        for date, temps in weather_data.items():
            year, month, _ = map(int, date.split("-"))
            monthly_data[year][month].append(temps["Mean"])
        
        return monthly_data

    def plot_boxplot(self, year_range):
        """
        Creates a boxplot of mean temperatures across all months in the specified year range.
        :param year_range: Tuple of two integers, start and end year.
        """
        data_for_plotting = []
        
        for month in range(1, 13):
            monthly_temps = []
            for year in range(year_range[0], year_range[1] + 1):
                monthly_temps.extend(self.weather_data.get(year, {}).get(month, []))
            data_for_plotting.append(monthly_temps)
        
        plt.figure(figsize=(10, 6))
        plt.boxplot(data_for_plotting, patch_artist=True)
        plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        plt.xlabel("Month")
        plt.ylabel("Mean Temperature")
        plt.title(f"Mean Temperatures from {year_range[0]} to {year_range[1]}")
        

    def plot_lineplot(self, month, year):
        """
        Creates a line plot for mean daily temperatures for a specific month and year.
        :param month: Integer representing the month (1-12).
        :param year: Integer representing the year.
        """
        data_for_month = self.weather_data.get(year, {}).get(month, [])
        
        if not data_for_month:
            print(f"No data available for {year}-{month:02d}.")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(data_for_month) + 1), data_for_month, marker='o', linestyle='-')
        plt.xlabel("Day")
        plt.ylabel("Mean Temperature")
        plt.title(f"Daily Mean Temperatures for {month}/{year}")
       

# Load and use the JSON data
with open("weather_data.json", "r") as file:
    weather_data = json.load(file)

plotter = PlotOperations(weather_data)
plotter.plot_boxplot((2020, 2024))  
plotter.plot_lineplot(12, 2020)     

plt.show()