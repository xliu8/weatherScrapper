from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="XXXXXX")

import openai
import json
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("weather_data.json", "r") as file:
    weather_data = json.load(file)

def format_weather_data(weather_data, max_entries=10):
    """Format the weather data for the prompt."""
    data_text = ""
    count = 0
    for date, temps in weather_data.items():
        if count >= max_entries:
            break
        data_text += f"{date}: Mean={temps['Mean']}, Max={temps['Max']}, Min={temps['Min']}\n"
        count += 1
    return data_text

date_to_predict = input("Enter the date to predict the temperature (e.g., 2024-01-01): ")
formatted_data = format_weather_data(weather_data)
prompt = f"Here is the historical data:\n{formatted_data}\n Predict max, min, and mean temperatures in Canada, on {date_to_predict}. Use typical seasonal patterns for this region, factoring in the likelihood of winter conditions. "



output = openai.completions.create(
    model = "gpt-3.5-turbo-instruct",
    prompt = prompt,
    max_tokens = 100,
    temperature = 0
)

print(output.choices[0].text.strip())
