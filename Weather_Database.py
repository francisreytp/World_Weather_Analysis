#%%
# Import the dependencies.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

import json 
import requests as req
from citipy import citipy

# Import the datetime module from the datetime library.
from datetime import datetime

# Import the API key.
from config import weather_api_key

# Import linear regression from the SciPy stats module.
from scipy.stats import linregress

#%%
# Create a set of random latitude and longitude combinations.
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)
lat_lngs 

#%%

# Add the latitudes and longitudes to a list.
coordinates = list(lat_lngs)
coordinates

#%%
# Starting URL for Weather Map API Call.
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + weather_api_key

#%%
# Create a list for holding the cities.
cities = []
# Identify the nearest city for each latitude and longitude combination.
for coordinate in coordinates:
    city = citipy.nearest_city(coordinate[0], coordinate[1]).city_name
    
    # If the city is unique, then we will add it to the cities list.
    if city not in cities:
        cities.append(city)
# Print the city count to confirm sufficient count.
len(cities)


#%%
# Create an empty list to hold the weather data.
# city_data = []
city_test = []

# Print the beginning of the logging.
print("Beginning Data Retrieval     ")
print("-----------------------------")
# Create counters.
record_count = 1
set_count = 1


# Loop through all the cities in the list.
for i, city in enumerate(cities):
    # Group cities in sets of 50 for logging purposes.
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 1
    # Create endpoint URL with each city.
    city_url = url + "&q=" + city

    # Log the URL, record, and set numbers and the city.
    print(f"Processing Record {record_count} of Set {set_count} | {city}")
    # Add 1 to the record count.
    record_count += 1
    # Run an API request for each of the cities.
    try:
        # Parse the JSON and retrieve data.
        city_weather = requests.get(city_url).json()
        # Parse out the needed data.
        # city_lat = city_weather["coord"]["lat"]
        # city_lng = city_weather["coord"]["lon"]
        # city_max_temp = city_weather["main"]["temp_max"]
        # city_humidity = city_weather["main"]["humidity"]
        # city_clouds = city_weather["clouds"]["all"]
        # city_wind = city_weather["wind"]["speed"]
        # city_country = city_weather["sys"]["country"]
        
        current_description = city_weather["weather"][0]["description"]
        try:
            current_rain = city_weather["rain"]["rain.3h"]
        except:
            current_rain = 0
            pass
        
        try:
            current_snow = city_weather["snow"]["snow.3h"]
        except:
            current_snow = 0
            pass
        # current_rain = 0
        # current_snow = 0
        # try:
        #     snow = city_weather["weather"][1]["main"]
        # except:
        #     snow = 0
        # Convert the date to ISO standard.
        city_date = datetime.utcfromtimestamp(city_weather["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        # Append the city information into city_data list.
        # city_data.append({"City": city.title(),
        #                   "Lat": city_lat,
        #                   "Lng": city_lng,
        #                   "Max Temp": city_max_temp,
        #                   "Humidity": city_humidity,
        #                   "Cloudiness": city_clouds,
        #                   "Wind Speed": city_wind,
        #                   "Country": city_country,
        #                   "Date": city_date})
                
        if current_rain > 0:
            city_test.append({"City": city.title(),
                        #   "Lat": city_lat,
                        #   "Lng": city_lng,
                        #   "Max Temp": city_max_temp,
                        #   "Humidity": city_humidity,
                        #   "Cloudiness": city_clouds,
                        #   "Wind Speed": city_wind,
                        #   "Country": city_country,
                        "Date": city_date,
                        "Current Description": current_description,
                        "Rain inches (last 3 hours)": current_rain,
                        "Snow inches (last 3 hours)": current_snow})

                                 
    # If an error is experienced, skip the city.
    except:
        print("City not found. Skipping...")
        pass
        # continue

# Indicate that Data Loading is complete.
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")

#%%
len(city_test)

#%%
city_test_df = pd.DataFrame(city_test)
city_test_df.tail(200)

# %%
len(city_data)

# %%
# Convert the array of dictionaries to a Pandas DataFrame.
city_data_df = pd.DataFrame(city_data)
city_data_df.head(10)

# %%
# Reorder the columns in the order you want them to appear.
new_column_order = ["City", "Country", "Date","Lat", "Lng", "Max Temp", "Humidity", "Cloudiness", "Wind Speed"] 

# Assign summary df the new column order.
city_data_df = city_data_df[new_column_order]
city_data_df


# %%
# Create the output file (CSV).
output_data_file = "weather_data/cities.csv"
# Export the City_Data into a CSV.
city_data_df.to_csv(output_data_file, index_label="City_ID")


#%%
# Files to load
cities_data_to_load = os.path.join("weather_data", "cities.csv")


#%%
# Read the file and store it in a Pandas DataFrame.
city_data_df = pd.read_csv(cities_data_to_load)
city_data_df

#%%
# Extract relevant fields from the DataFrame for plotting.
lats = city_data_df["Lat"]
max_temps = city_data_df["Max Temp"]
humidity = city_data_df["Humidity"]
cloudiness = city_data_df["Cloudiness"]
wind_speed = city_data_df["Wind Speed"]


