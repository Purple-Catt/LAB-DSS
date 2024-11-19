import os
from geopy.geocoders import Nominatim

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Copies are used to preserve the original datasets
people = open(ROOT_DIR + '/Data/People - Copy.csv', 'r')
crashes = open(ROOT_DIR + '/Data/Crashes - Copy.csv', 'r')
vehicles = open(ROOT_DIR + '/Data/Vehicles - Copy.csv', 'r')

people_lines = people.readlines()
crashes_lines = crashes.readlines()
vehicles_lines = vehicles.readlines()

people.close()
crashes.close()
vehicles.close()

people = open(ROOT_DIR + '/Data/People - Copy.csv', 'w')
crashes = open(ROOT_DIR + '/Data/Crashes - Copy.csv', 'w')
# vehicles = open(ROOT_DIR + '/Data/Vehicles - Copy.csv', 'w')

people_columns = people_lines.pop(0).split(',')
crashes_columns = crashes_lines.pop(0).split(',')
vehicles_columns = vehicles_lines.pop(0).split(',')

for idx, line in enumerate(people_lines):
    # Skip the first line that contains the columns names

    split_line = line.split(',')
    # VEHICLE_ID null means that the person is PEDESTRIAN, BICYCLE or NON-MOTOR VEHICLE, so it can be labelled as 0
    if split_line[people_columns.index('VEHICLE_ID')] == '':
        split_line[people_columns.index('VEHICLE_ID')] = '0'

    # SEX null values can be labelled as X
    if split_line[people_columns.index('SEX')] == '':
        split_line[people_columns.index('SEX')] = 'X'

    # SAFETY_EQUIPMENT null values can be labelled as USAGE UNKNOWN
    if split_line[people_columns.index('SAFETY_EQUIPMENT')] == '':
        split_line[people_columns.index('SAFETY_EQUIPMENT')] = 'USAGE UNKNOWN'

    # AIRBAG_DEPLOYED null values can be labelled as DEPLOYMENT UNKNOWN
    if split_line[people_columns.index('AIRBAG_DEPLOYED')] == '':
        split_line[people_columns.index('AIRBAG_DEPLOYED')] = 'DEPLOYMENT UNKNOWN'

    # EJECTION null values can be labelled as UNKNOWN
    if split_line[people_columns.index('EJECTION')] == '':
        split_line[people_columns.index('EJECTION')] = 'UNKNOWN'

    # DRIVER_ACTION null values can be labelled as UNKNOWN
    if split_line[people_columns.index('DRIVER_ACTION')] == '':
        split_line[people_columns.index('DRIVER_ACTION')] = 'UNKNOWN'

    # DRIVER_VISION null values can be labelled as UNKNOWN
    if split_line[people_columns.index('DRIVER_VISION')] == '':
        split_line[people_columns.index('DRIVER_VISION')] = 'UNKNOWN'

    # PHYSICAL_CONDITION null values can be labelled as UNKNOWN
    if split_line[people_columns.index('PHYSICAL_CONDITION')] == '':
        split_line[people_columns.index('PHYSICAL_CONDITION')] = 'UNKNOWN'

    people_lines[idx] = ','.join(split_line)

people.write(','.join(people_columns))
people.writelines(people_lines)

# Switch to Crashes dataset
geolocator = Nominatim(user_agent="marcodelpi@hotmail.com")

for idx, line in enumerate(crashes_lines):
    split_line = line.split(',')

    if split_line[crashes_columns.index('LATITUDE')] == '':
        addr = (f"{split_line[crashes_columns.index('STREET_NO')]} {split_line[crashes_columns.index('STREET_NAME')]}, "
                f"Chicago, IL, United States")
        location = geolocator.geocode(addr)
        if location:
            split_line[crashes_columns.index('LATITUDE')] = str(location.latitude)
            split_line[crashes_columns.index('LONGITUDE')] = str(location.longitude)
            print(f"Address {addr} retrieved successfully")

        else:
            print(f"Unable to retrieve location for address: {addr}")

    crashes_lines[idx] = ','.join(split_line)

crashes.write(','.join(crashes_columns))
crashes.writelines(crashes_lines)

people.close()
crashes.close()
vehicles.close()
