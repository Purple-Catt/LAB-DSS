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
vehicles = open(ROOT_DIR + '/Data/Vehicles - Copy.csv', 'w')

people_columns = people_lines.pop(0).split(',')
crashes_columns = crashes_lines.pop(0).split(',')
vehicles_columns = vehicles_lines.pop(0).split(',')

# Computing mode for attribute AGE
mode = dict()

for idx, line in enumerate(people_lines):
    split_line = line.split(',')
    try:
        mode[split_line[people_columns.index('AGE')]] += 1

    except KeyError:
        mode[split_line[people_columns.index('AGE')]] = 1

mode.pop('')
mx = 0
max_k = 0
for k, v in mode.items():
    if v > mx:
        mx = v
        max_k = k

people_col_to_drop = list()
states = dict()
for idx, line in enumerate(people_lines):
    split_line = line.split(',')
    temp = ''
    spare = 0
    new_idx = 0
    merge = False
    drop_col = list()
    for col_idx, item in enumerate(split_line):
        if merge:
            temp = temp + ',' + item
            drop_col.append(col_idx)
            if '"' in item and '""' not in item:
                spare = 0
                merge = False
                split_line[new_idx] = temp
                temp = ''
                continue

        if '"' in item and '""' not in item:
            if spare == 0:
                temp += item
                spare = 1
                merge = True
                new_idx = col_idx
    for c in reversed(drop_col):
        split_line.pop(c)

    # Check correctness of the previous for loop results
    if len(split_line) != len(people_columns):
        raise IndexError

    split_line[people_columns.index('PERSON_ID')] = split_line[people_columns.index('PERSON_ID')].removeprefix('P')
    split_line[people_columns.index('PERSON_ID')] = split_line[people_columns.index('PERSON_ID')].removeprefix('O')

    # VEHICLE_ID null means that the person is PEDESTRIAN, BICYCLE or NON-MOTOR VEHICLE, so it can be labelled as 0
    if split_line[people_columns.index('VEHICLE_ID')] == '':
        split_line[people_columns.index('VEHICLE_ID')] = '0'

    # SEX null values can be labelled as X
    if split_line[people_columns.index('SEX')] == '':
        split_line[people_columns.index('SEX')] = 'X'

    # AGE null values can be substituted using the mode
    if split_line[people_columns.index('AGE')] == '':
        split_line[people_columns.index('AGE')] = max_k

    # CITY and STATE can be substituted with Chicago, IL, given that almost all the people are from there
    if split_line[people_columns.index('CITY')] == '':
        split_line[people_columns.index('CITY')] = 'CHICAGO'

    if split_line[people_columns.index('STATE')] == '':
        split_line[people_columns.index('STATE')] = 'IL'

    states[split_line[people_columns.index('PERSON_ID')]] = split_line[people_columns.index('STATE')]

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

    # BAC_RESULT null values can be substituted with TEST NOT OFFERED
    if split_line[people_columns.index('BAC_RESULT')] == '':
        split_line[people_columns.index('BAC_RESULT')] = 'TEST NOT OFFERED'

    # DAMAGE null values can be set to 0
    if split_line[people_columns.index('DAMAGE\n')] == '\n':
        split_line[people_columns.index('DAMAGE\n')] = '0\n'

    if split_line[people_columns.index('INJURY_CLASSIFICATION')] == '':
        people_col_to_drop.append(idx)

    else:
        people_lines[idx] = ','.join(split_line)

for c in sorted(people_col_to_drop, reverse=True):
    people_lines.pop(c)

people.write(','.join(people_columns))
people.writelines(people_lines)

# Switch to Crashes dataset
geolocator = Nominatim(user_agent="marcodelpi@hotmail.com")

crashes_col_to_drop = list()
for idx, line in enumerate(crashes_lines):
    split_line = line.split(',')
    temp = ''
    spare = 0
    new_idx = 0
    merge = False
    drop_col = list()
    for col_idx, item in enumerate(split_line):
        if merge:
            temp = temp + ',' + item
            drop_col.append(col_idx)
            if '"' in item and '""' not in item:
                spare = 0
                merge = False
                split_line[new_idx] = temp
                temp = ''
                continue

        if '"' in item and '""' not in item:
            if spare == 0:
                temp += item
                spare = 1
                merge = True
                new_idx = col_idx
    for c in reversed(drop_col):
        split_line.pop(c)

    # Check correctness of the previous for loop results
    if len(split_line) != len(crashes_columns):
        raise IndexError

    if split_line[crashes_columns.index('LATITUDE')] == '':
        addr = (f"{split_line[crashes_columns.index('STREET_NO')]} {split_line[crashes_columns.index('STREET_NAME')]}, "
                f"Chicago, IL, United States")
        try:
            location = geolocator.geocode(addr)
        except:
            print("Error occurred")
            location = None

        if location:
            split_line[crashes_columns.index('LATITUDE')] = str(location.latitude)
            split_line[crashes_columns.index('LONGITUDE')] = str(location.longitude)
            split_line[crashes_columns.index('LOCATION\n')] = f'POINT ({str(location.longitude)} {str(location.latitude)})\n'
            print(f"Address {addr} retrieved successfully")

        else:
            print(f"Unable to retrieve location for address: {addr}")
    
    if split_line[crashes_columns.index('REPORT_TYPE')] == '':
        split_line[crashes_columns.index('REPORT_TYPE')] = 'UNKNOWN'
        
    if (split_line[crashes_columns.index('STREET_DIRECTION')] == '' or
            split_line[crashes_columns.index('STREET_NAME')] == '' or
            split_line[crashes_columns.index('BEAT_OF_OCCURRENCE')] == '' or
            split_line[crashes_columns.index('MOST_SEVERE_INJURY')] == '' or
            split_line[crashes_columns.index('LONGITUDE')] == ''):
        crashes_col_to_drop.append(idx)

    else:
        crashes_lines[idx] = ','.join(split_line)

for c in sorted(crashes_col_to_drop, reverse=True):
    crashes_lines.pop(c)

crashes.write(','.join(crashes_columns))
crashes.writelines(crashes_lines)

# Switch to Vehicles dataset
vehicles_col_to_drop = list()
for idx, line in enumerate(vehicles_lines):
    split_line = line.split(',')
    temp = ''
    spare = 0
    new_idx = 0
    merge = False
    drop_col = list()
    for col_idx, item in enumerate(split_line):
        if merge:
            temp = temp + ',' + item
            drop_col.append(col_idx)
            if '"' in item and '""' not in item:
                spare = 0
                merge = False
                split_line[new_idx] = temp
                temp = ''
                continue

        if '"' in item and '""' not in item:
            if spare == 0:
                temp += item
                spare = 1
                merge = True
                new_idx = col_idx

    for c in reversed(drop_col):
        split_line.pop(c)

    # Check correctness of the previous for loop results
    if len(split_line) != len(vehicles_columns):
        # raise IndexError
        print(f'Error occurred. Line of length {len(split_line)} instead of {len(vehicles_columns)}')
        vehicles_col_to_drop.append(idx)

    # where UNIT_TYPE is not PEDESTRIAN, BICYCLE or NON-MOTOR VEHICLE, MODEL and FIRST_CONTACT_POINT can be labelled as UNKNOWN
    if split_line[vehicles_columns.index('UNIT_TYPE')] not in ['PEDESTRIAN', 'BICYCLE', 'NON-MOTOR VEHICLE'] and split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] == '\n':
        split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] = 'UNKNOWN\n'

    if split_line[vehicles_columns.index('UNIT_TYPE')] in ['PEDESTRIAN', 'BICYCLE', 'NON-MOTOR VEHICLE']:
        if split_line[vehicles_columns.index('VEHICLE_ID')] == '':
            split_line[vehicles_columns.index('VEHICLE_ID')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('MAKE')] == '':
            split_line[vehicles_columns.index('MAKE')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('MODEL')] == '':
            split_line[vehicles_columns.index('MODEL')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('LIC_PLATE_STATE')] == '':
            split_line[vehicles_columns.index('LIC_PLATE_STATE')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('VEHICLE_YEAR')] == '':
            split_line[vehicles_columns.index('VEHICLE_YEAR')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('VEHICLE_DEFECT')] == '':
            split_line[vehicles_columns.index('VEHICLE_DEFECT')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('VEHICLE_TYPE')] == '':
            split_line[vehicles_columns.index('VEHICLE_TYPE')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('VEHICLE_USE')] == '':
            split_line[vehicles_columns.index('VEHICLE_USE')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('TRAVEL_DIRECTION')] == '':
            split_line[vehicles_columns.index('TRAVEL_DIRECTION')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('MANEUVER')] == '':
            split_line[vehicles_columns.index('MANEUVER')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('OCCUPANT_CNT')] == '':
            split_line[vehicles_columns.index('OCCUPANT_CNT')] = 'NOT_A_VEHICLE'
        if split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] == '\n':
            split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] = 'NOT_A_VEHICLE\n'

    if split_line[vehicles_columns.index('MODEL')] == '':
        split_line[vehicles_columns.index('MODEL')] = 'UNKNOWN'

    if split_line[vehicles_columns.index('UNIT_TYPE')] == '':
        vehicles_col_to_drop.append(idx)

    # This if statement exists because 48 records contains no information at all regarding the vehicles so,
    # instead of substitute all the null values it's better to remove them
    if split_line[vehicles_columns.index('VEHICLE_ID')] == '':
        vehicles_col_to_drop.append(idx)

    if split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] == '\n':
        split_line[vehicles_columns.index('FIRST_CONTACT_POINT\n')] = 'UNKNOWN\n'

    if split_line[vehicles_columns.index('LIC_PLATE_STATE')] == '':
        try:
            split_line[vehicles_columns.index('LIC_PLATE_STATE')] = states[split_line[vehicles_columns.index('CRASH_UNIT_ID')]]
        except KeyError:
            split_line[vehicles_columns.index('LIC_PLATE_STATE')] = 'UNKNOWN'

    if split_line[vehicles_columns.index('VEHICLE_YEAR')] == '':
        split_line[vehicles_columns.index('VEHICLE_YEAR')] = '2015'

    try:
        yr = float(split_line[vehicles_columns.index('VEHICLE_YEAR')])
    except ValueError:
        yr = 0

    if yr > 2019.0:
        vehicles_col_to_drop.append(idx)
    else:
        vehicles_lines[idx] = ','.join(split_line)

for c in sorted(vehicles_col_to_drop, reverse=True):
    vehicles_lines.pop(c)

vehicles.write(','.join(vehicles_columns))
vehicles.writelines(vehicles_lines)

people.close()
crashes.close()
vehicles.close()
