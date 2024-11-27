import csv
from datetime import datetime

# Extract and process data for Date_Dim
with open('/mnt/data/Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    date_dim = []
    unique_dates = set()

    for row in reader:
        crash_date = row['CrashDate']
        crash_time = row.get('CrashTime', '00:00')
        if crash_date not in unique_dates:
            unique_dates.add(crash_date)
            date_obj = datetime.strptime(crash_date, '%Y-%m-%d')
            hour = int(crash_time.split(':')[0])
            time_of_day = (
                "Morning" if 6 <= hour < 12 else
                "Afternoon" if 12 <= hour < 18 else
                "Evening" if 18 <= hour < 24 else
                "Night"
            )
            is_weekend = 1 if date_obj.weekday() >= 5 else 0
            date_dim.append([
                crash_date,
                date_obj.year,
                (date_obj.month - 1) // 3 + 1,  # Quarter
                date_obj.month,
                date_obj.day,
                date_obj.strftime("%A"),
                is_weekend,
                hour,
                time_of_day
            ])

# Save to Date_Dim.csv
with open('Date_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Date_ID', 'Full_Date', 'Year', 'Quarter', 'Month', 'Day', 'Weekday', 'Is_Weekend', 'Hour', 'Time_Of_Day'])
    for idx, row in enumerate(date_dim, start=1):
        writer.writerow([idx] + row)
# Extract and process data for Vehicle_Dim
with open('/mnt/data/Vehicles.csv', 'r') as vehicles_file:
    reader = csv.DictReader(vehicles_file)
    vehicle_dim = []
    unique_vehicles = set()

    for row in reader:
        vehicle = (row['VehicleMake'], row['VehicleModel'], row['VehicleYear'], row['VehicleType'], row.get('Color', 'Unknown'), row.get('FuelType', 'Unknown'), row.get('PassengerCapacity', 0), row.get('IsCommercial', 0))
        if vehicle not in unique_vehicles:
            unique_vehicles.add(vehicle)
            vehicle_dim.append(vehicle)

# Save to Vehicle_Dim.csv
with open('Vehicle_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Vehicle_ID', 'Make', 'Model', 'Year', 'Vehicle_Type', 'Color', 'Fuel_Type', 'Passenger_Capacity', 'Is_Commercial'])
    for idx, row in enumerate(vehicle_dim, start=1):
        writer.writerow([idx] + list(row))
# Extract and process data for Geography_Dim
with open('/mnt/data/Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    geography_dim = []
    unique_locations = set()

    for row in reader:
        location = (row['Street'], row['City'], row['State'], row['ZipCode'], row.get('Region', 'Unknown'), row.get('Latitude', None), row.get('Longitude', None))
        if location not in unique_locations:
            unique_locations.add(location)
            geography_dim.append(location)

# Save to Geography_Dim.csv
with open('Geography_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Location_ID', 'Street', 'City', 'State', 'Zip_Code', 'Region', 'Latitude', 'Longitude'])
    for idx, row in enumerate(geography_dim, start=1):
        writer.writerow([idx] + list(row))
# Extract and process data for Crash_Dim
with open('/mnt/data/Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    crash_dim = []
    unique_crashes = set()

    for row in reader:
        crash = (row['CrashType'], row['SeverityLevel'], row['LightConditions'], row['RoadConditions'], row['TrafficControl'], row.get('IsHitAndRun', 0))
        if crash not in unique_crashes:
            unique_crashes.add(crash)
            crash_dim.append(crash)

# Save to Crash_Dim.csv
with open('Crash_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Crash_ID', 'Crash_Type', 'Severity_Level', 'Light_Conditions', 'Road_Conditions', 'Traffic_Control', 'Is_Hit_And_Run'])
    for idx, row in enumerate(crash_dim, start=1):
        writer.writerow([idx] + list(row))
# Extract and process data for Person_Dim
with open('/mnt/data/People.csv', 'r') as people_file:
    reader = csv.DictReader(people_file)
    person_dim = []
    unique_people = set()

    for row in reader:
        person = (row['PersonAge'], row['PersonGender'], row['Role'], row['InjuryLevel'], row.get('IsImpaired', 0), row.get('LicenseStatus', 'Unknown'), row.get('IsResident', 0))
        if person not in unique_people:
            unique_people.add(person)
            person_dim.append(person)

# Save to Person_Dim.csv
with open('Person_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Person_ID', 'Age', 'Gender', 'Role', 'Injury_Level', 'Is_Impaired', 'License_Status', 'Is_Resident'])
    for idx, row in enumerate(person_dim, start=1):
        writer.writerow([idx] + list(row))
# Extract and process data for Weather_Dim
with open('/mnt/data/Crashes.csv', 'r') as crashes_file:
    reader = csv.DictReader(crashes_file)
    weather_dim = []
    unique_weather = set()

    for row in reader:
        weather = (row['WeatherCondition'], row['Temperature'], row['Visibility'], row['WindSpeed'], row['Precipitation'], row['Humidity'])
        if weather not in unique_weather:
            unique_weather.add(weather)
            weather_dim.append(weather)

# Save to Weather_Dim.csv
with open('Weather_Dim.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Weather_ID', 'Condition', 'Temperature', 'Visibility', 'Wind_Speed', 'Precipitation', 'Humidity'])
    for idx, row in enumerate(weather_dim, start=1):
        writer.writerow([idx] + list(row))
# Combine all dimensions into the Fact Table
with open('/mnt/data/Crashes.csv', 'r') as crashes_file:
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
with open('Damage_Fact.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Damage_ID', 'Date_ID', 'Location_ID', 'Vehicle_ID', 'Person_ID', 'Weather_ID', 'Cause_ID', 'Road_ID', 'Driver_Behavior_ID', 'Damage_Cost', 'Num_Units'])
    for idx, row in enumerate(fact_table, start=1):
        writer.writerow([idx] + row)
