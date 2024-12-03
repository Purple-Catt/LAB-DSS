import csv
import os
from datetime import datetime
import openmeteo_requests
import requests_cache
from retry_requests import retry

# TODO crash dim
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = f'{ROOT_DIR}/Data/'
DIM_PATH = f'{ROOT_DIR}/Data/DW/'

# Extract and process data for Date_Dim
with open(f'{RAW_PATH}Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    date_dim = []
    unique_dates = set()
    for row in reader:
        crash_datetime = datetime.strptime(row['CRASH_DATE'], '%m/%d/%Y %I:%M:%S %p')
        crash_date = datetime.strftime(crash_datetime, '%Y-%m-%d')
        crash_hour = int(datetime.strftime(crash_datetime, '%H'))
        if crash_date not in unique_dates:
            unique_dates.add(crash_date)
            time_of_day = (
                "Morning" if 6 <= crash_hour < 12 else
                "Afternoon" if 12 <= crash_hour < 18 else
                "Evening" if 18 <= crash_hour < 24 else
                "Night"
            )
            is_weekend = 1 if crash_datetime.weekday() >= 5 else 0
            date_dim.append([
                crash_date,
                crash_datetime.year,
                (crash_datetime.month - 1) // 3 + 1,  # Quarter
                crash_datetime.month,
                crash_datetime.day,
                crash_datetime.strftime("%A"),
                is_weekend,
                crash_hour,
                time_of_day
            ])

# Save to Date_Dim.csv
with open(f'{DIM_PATH}Date_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Date_ID', 'Full_Date', 'Year', 'Quarter', 'Month', 'Day', 'Weekday', 'Is_Weekend', 'Hour', 'Time_Of_Day'])
    for idx, row in enumerate(date_dim, start=1):
        writer.writerow([idx] + row)

# Extract and process data for Vehicle_Dim
with open(f'{RAW_PATH}Vehicles.csv', 'r') as vehicles_file:
    reader = csv.DictReader(vehicles_file)
    vehicle_dim = []
    unique_vehicles = set()

    for row in reader:
        vehicle = (row['MAKE'], row['MODEL'], row['VEHICLE_YEAR'], row['VEHICLE_TYPE'])
        if vehicle not in unique_vehicles:
            unique_vehicles.add(vehicle)
            vehicle_dim.append(vehicle)

# Save to Vehicle_Dim.csv
with open(f'{DIM_PATH}Vehicle_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Vehicle_ID', 'Make', 'Model', 'Year', 'Vehicle_Type'])
    for idx, row in enumerate(vehicle_dim, start=1):
        writer.writerow([idx] + list(row))

# Extract and process data for Geography_Dim
with open(f'{RAW_PATH}Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    geography_dim = []
    unique_locations = set()

    for row in reader:
        location = (row['STREET_NAME'], row['STREET_NO'], row.get('LATITUDE', None), row.get('LONGITUDE', None))
        if location not in unique_locations:
            unique_locations.add(location)
            geography_dim.append(location)

# Save to Geography_Dim.csv
with open(f'{DIM_PATH}Geography_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Location_ID', 'Street', 'Street_no', 'Latitude', 'Longitude'])
    for idx, row in enumerate(geography_dim, start=1):
        writer.writerow([idx] + list(row))

# Extract and process data for Crash_Dim
with open(f'{RAW_PATH}Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    crash_dim = []
    unique_crashes = set()

    for row in reader:
        crash = (row['CRASH_TYPE'], row['MOST_SEVERE_INJURY'], row['LIGHTING_CONDITION'], row['ROADWAY_SURFACE_COND'], row['TRAFFIC_CONTROL_DEVICE'])
        if crash not in unique_crashes:
            unique_crashes.add(crash)
            crash_dim.append(crash)

# Save to Crash_Dim.csv
with open(f'{DIM_PATH}Crash_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Crash_ID', 'Crash_Type', 'Severity_Level', 'Light_Conditions', 'Road_Conditions', 'Traffic_Control'])
    for idx, row in enumerate(crash_dim, start=1):
        writer.writerow([idx] + list(row))

# Extract and process data for Person_Dim
with open(f'{RAW_PATH}People.csv', 'r') as people_file:
    reader = csv.DictReader(people_file)
    person_dim = []
    unique_people = set()

    for row in reader:
        resident = 1 if row['CITY'] == 'CHICAGO' else 0
        is_impaired = 1 if 'IMPAIRED' in row['PHYSICAL_CONDITION'] else 0
        person = (row['AGE'], row['SEX'], row['PERSON_TYPE'], row['INJURY_CLASSIFICATION'], is_impaired, resident)
        if person not in unique_people:
            unique_people.add(person)
            person_dim.append(person)

# Save to Person_Dim.csv
with open(f'{DIM_PATH}Person_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Person_ID', 'Age', 'Gender', 'Role', 'Injury_Level', 'Is_Impaired', 'Is_Resident'])
    for idx, row in enumerate(person_dim, start=1):
        writer.writerow([idx] + list(row))

# Extract and process data for Driver_Behavior_Dim
with open(f'{RAW_PATH}People.csv', 'r', newline='') as people_file:
    reader = csv.DictReader(people_file)
    behavior_dim = []
    unique_behavior = set()

    for row in reader:
        behavior = (row['DRIVER_ACTION'])

        if behavior not in unique_behavior:
            unique_behavior.add(behavior)
            behavior_dim.append(behavior)

# Save to Driver_Behavior_Dim.csv
with open(f'{DIM_PATH}Driver_Behavior_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Behavior_ID', 'Driver_Action'])
    for idx, row in enumerate(behavior_dim, start=1):
        writer.writerow([idx] + list(row))

'''
    Extract and process data for Weather_Dim
with open(f'{RAW_PATH}Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    weather_dim = []
    unique_weather = set()
    # Set up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    for row in reader:
        crash_datetime = datetime.strptime(row['CRASH_DATE'], '%m/%d/%Y %I:%M:%S %p')
        crash_date = datetime.strftime(crash_datetime, '%Y-%m-%d')
        crash_hour = int(datetime.strftime(crash_datetime, '%H'))
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": float(row['LATITUDE']),
            "longitude": float(row['LONGITUDE']),
            "start_date": crash_date,
            "end_date": crash_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "weather_code", "precipitation", "cloud_cover", "wind_speed_10m"]
        }
        # Retrieve data for the given hour
        response_hourly = openmeteo.weather_api(url, params=params)[0].Hourly()

        temperature = response_hourly.Variables(0).ValuesAsNumpy()[crash_hour]
        humidity = response_hourly.Variables(1).ValuesAsNumpy()[crash_hour]
        w_code = response_hourly.Variables(2).ValuesAsNumpy()[crash_hour]
        precipitation = response_hourly.Variables(3).ValuesAsNumpy()[crash_hour]
        cloud = response_hourly.Variables(4).ValuesAsNumpy()[crash_hour]
        wind = response_hourly.Variables(5).ValuesAsNumpy()[crash_hour]
        # Decoding weather conditions
        wmo_dict = {
            0: 'CLEAR',
            1: 'PARTLY_CLOUDY', 2: 'PARTLY_CLOUDY', 3: 'PARTLY_CLOUDY',
            45: 'FOG', 48: 'FOG',
            51: 'DRIZZLE', 53: 'DRIZZLE', 55: 'DRIZZLE',
            56: 'FREEZING_DRIZZLE', 57: 'FREEZING_DRIZZLE',
            61: 'RAIN', 63: 'RAIN', 65: 'RAIN',
            66: 'FREEZING_RAIN', 67: 'FREEZING_RAIN',
            71: 'SNOW_FALL', 73: 'SNOW_FALL', 75: 'SNOW_FALL',
            77: 'SNOW_GRAINS',
            80: 'RAIN_SHOWERS', 81: 'RAIN_SHOWERS', 82: 'RAIN_SHOWERS',
            85: 'SNOW_SHOWERS', 86: 'SNOW_SHOWERS'
        }
        condition = wmo_dict[w_code]

        weather = (condition, temperature, cloud, wind, precipitation, humidity)
        if weather not in unique_weather:
            unique_weather.add(weather)
            weather_dim.append(weather)

    # Save to Weather_Dim.csv
with open(f'{DIM_PATH}Weather_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Weather_ID', 'Condition', 'Temperature', 'Cloud_Cover', 'Wind_Speed', 'Precipitation', 'Humidity'])
    for idx, row in enumerate(weather_dim, start=1):
        writer.writerow([idx] + list(row))ù
'''
'''
Combine all dimensions into the Fact Table
with open(f'{RAW_PATH}Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    fact_table = []

    for row in reader:
        fact_table.append([
            row['CrashID'],  # Damage_ID
            row['CrashDate'],  # Date_ID (link to Date_Dim)
            row['Street'],  # Location_ID (link to Geography_Dim)
            row['VehicleID'],  # Vehicle_ID (link to Vehicle_Dim)
            row['PersonID'],  # Person_ID (link to Person_Dim)
            row['WeatherID'],  # Weather_ID (link to Weather_Dim)
            row['CauseID'],  # Cause_ID (link to Cause_Dim)
            row['RoadID'],  # Road_ID (link to Road_Dim)
            row['DriverBehaviorID'],  # Driver_Behavior_ID (link to Driver_Behavior_Dim)
            row['DamageCost'],  # Damage cost
            row['NumUnits']  # Number of units involved
        ])

# Save to Damage_Fact.csv
with open(f'{DIM_PATH}Damage_Fact.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Damage_ID', 'Date_ID', 'Location_ID', 'Vehicle_ID', 'Person_ID', 'Weather_ID', 'Cause_ID', 'Road_ID', 'Driver_Behavior_ID', 'Damage_Cost', 'Num_Units'])
    for idx, row in enumerate(fact_table, start=1):
        writer.writerow([idx] + row)
'''