import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Copies are used to preserve the original datasets
people_path = ROOT_DIR + '/Data/People - Copy.csv'
crashes_path = ROOT_DIR + '/Data/Crashes - Copy.csv'
vehicles_path = ROOT_DIR + '/Data/Vehicles - Copy.csv'

reimbursement_path = ROOT_DIR + '/Data/DW/Reimbursement.csv'
person_path = ROOT_DIR + '/Data/DW/Person.csv'
crash_path = ROOT_DIR + '/Data/DW/Crash.csv'
vehicle_path = ROOT_DIR + '/Data/DW/Vehicle.csv'
date_path = ROOT_DIR + '/Data/DW/Date.csv'
geography_path = ROOT_DIR + '/Data/DW/Geography.csv'


def filter_columns(input_path: str, output_path: str, columns_to_drop: list):
    with open(input_path,'r') as inpath:
        lines = inpath.readlines()

    # Split lines into columns and filter
    header = lines[0].strip().split(',')
    filtered_header = header.copy()
    columns_to_drop_idx = [filtered_header.index(i) for i in columns_to_drop]
    for i in columns_to_drop:
        filtered_header.remove(i)

    filtered_lines = [','.join(filtered_header) + '\n']  # Start with filtered header

    # Filter data rows
    for line in lines[1:]:
        row = line.strip().split(',')
        filtered_row = list()
        for i in range(len(header)):
            if i not in columns_to_drop_idx:
                filtered_row.append(row[i])
        filtered_lines.append(','.join(filtered_row) + '\n')

    # Write to new file
    with open(output_path, 'x') as outpath:
        outpath.writelines(filtered_lines)


filter_columns(input_path=people_path, output_path=person_path,
               columns_to_drop=['CRASH_DATE', 'DAMAGE_CATEGORY', 'DAMAGE', 'PHYSICAL_CONDITION', 'VEHICLE_ID',
                                'INJURY_CLASSIFICATION', 'SAFETY_EQUIPMENT', 'AIRBAG_DEPLOYED', 'EJECTION',
                                'DRIVER_ACTION', 'DRIVER_VISION', 'BAC_RESULT'])
filter_columns(input_path=crashes_path, output_path=crash_path,
               columns_to_drop=['CRASH_DATE', 'STREET_NO', 'STREET_DIRECTION', 'STREET_NAME', 'NUM_UNITS',
                                'INJURIES_TOTAL', 'INJURIES_FATAL', 'INJURIES_INCAPACITATING',
                                'INJURIES_NON_INCAPACITATING', 'INJURIES_REPORTED_NOT_EVIDENT',
                                'INJURIES_NO_INDICATION', 'INJURIES_UNKNOWN', 'LATITUDE', 'LONGITUDE', 'LOCATION'])
filter_columns(input_path=vehicles_path, output_path=vehicle_path, columns_to_drop=['CRASH_DATE'])
filter_columns(input_path=people_path, output_path=reimbursement_path,
               columns_to_drop=['CRASH_DATE', 'PERSON_TYPE', 'CITY', 'STATE', 'SEX', 'AGE'])
filter_columns(input_path=crashes_path, output_path=geography_path,
               columns_to_drop=['CRASH_DATE', 'POSTED_SPEED_LIMIT', 'TRAFFIC_CONTROL_DEVICE', 'DEVICE_CONDITION',
                                'WEATHER_CONDITION', 'LIGHTING_CONDITION', 'FIRST_CRASH_TYPE', 'TRAFFICWAY_TYPE',
                                'ALIGNMENT', 'ROADWAY_SURFACE_COND', 'ROAD_DEFECT', 'REPORT_TYPE', 'CRASH_TYPE',
                                'DATE_POLICE_NOTIFIED', 'PRIM_CONTRIBUTORY_CAUSE', 'SEC_CONTRIBUTORY_CAUSE',
                                'BEAT_OF_OCCURRENCE', 'NUM_UNITS', 'MOST_SEVERE_INJURY', 'INJURIES_TOTAL',
                                'INJURIES_FATAL', 'INJURIES_INCAPACITATING','INJURIES_NON_INCAPACITATING',
                                'INJURIES_REPORTED_NOT_EVIDENT', 'INJURIES_NO_INDICATION', 'INJURIES_UNKNOWN',
                                'CRASH_HOUR', 'CRASH_DAY_OF_WEEK', 'CRASH_MONTH'])
