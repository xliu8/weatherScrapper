# Python_Weather_App

## Scrapping

This Python script is designed to scrape historical daily weather data from a Canadian government weather website. The data extraction starts from the current date and goes back in time, iterating month by month until the earliest available data on the site is reached. The goal is to capture daily maximum, minimum, and mean temperatures.

Known Issue: Despite the systematic approach, some weather data points might still be missing. This could be due to various factors such as incomplete data on the website, changes in the website structure, or limitations in how the parser handles the content. Debugging and improving data handling can help address these gaps.

Functionality Overview:

WeatherScraper Class: A custom HTML parser that processes HTML content to extract weather data.
Data Extraction: Begins with the current month and year, moving backward in time month by month until no "previous month" link is found.
Output: Collected weather data is printed as a dictionary, where each key is a date, and values include temperatures (max, min, mean).

Potential Areas for Debugging Missing Data:

1. HTML Structure Changes: Verify if the structure of the weather data pages has changed over time, which could affect data parsing.
2. Incomplete or Corrupted Data: Check if certain months or days lack full data sets (e.g., missing temperatures).
3. Error Handling and Skipping: Ensure the script doesn’t skip entries due to unexpected data formats or empty fields.
4. Request Limitations: Confirm that the site doesn’t block or throttle repeated requests, which could lead to missing data.
