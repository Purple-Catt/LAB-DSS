CREATE TABLE Date_Dim (
                          Date_ID INT PRIMARY KEY, -- Unique identifier for the date
                          Full_Date DATE, -- Full date (e.g., "2024-11-26")
                          Year INT, -- Year of the date
                          Quarter INT, -- Quarter of the year (1-4)
                          Month INT, -- Month of the year (1-12)
                          Day INT, -- Day of the month (1-31)
                          Weekday VARCHAR(20), -- Name of the weekday (e.g., "Monday")
                          Is_Weekend BIT, -- Indicates if the date is a weekend (1 for yes, 0 for no)
                          Hour INT, -- Hour of the accident (0-23)
                          Time_Of_Day VARCHAR(20) -- Time of the day (e.g., "Morning", "Evening")
);
CREATE TABLE Vehicle_Dim (
                             Vehicle_ID INT PRIMARY KEY, -- Unique identifier for the vehicle
                             Make VARCHAR(50), -- Vehicle manufacturer (e.g., "Toyota")
                             Model VARCHAR(50), -- Vehicle model (e.g., "Corolla")
                             Year INT, -- Year of manufacture
                             Vehicle_Type VARCHAR(50), -- Type of vehicle (e.g., "SUV", "Truck")
                             Color VARCHAR(20), -- Color of the vehicle (e.g., "Red")
                             Fuel_Type VARCHAR(20), -- Type of fuel (e.g., "Gasoline", "Electric")
                             Passenger_Capacity INT, -- Number of passengers the vehicle can hold
                             Is_Commercial BIT -- Indicates if the vehicle is commercial (1 for yes, 0 for no)
);
CREATE TABLE Geography_Dim (
                               Location_ID INT PRIMARY KEY, -- Unique identifier for the location
                               Street VARCHAR(255), -- Street name
                               City VARCHAR(255), -- City name
                               State VARCHAR(50), -- State name
                               Zip_Code VARCHAR(10), -- Postal code
                               Region VARCHAR(50), -- Region within the city/state (e.g., "North", "South")
                               Latitude DECIMAL(9,6), -- Latitude coordinate
                               Longitude DECIMAL(9,6) -- Longitude coordinate
);
CREATE TABLE Crash_Dim (
                           Crash_ID INT PRIMARY KEY, -- Unique identifier for the crash
                           Crash_Type VARCHAR(50), -- Type of crash (e.g., "Rear-End", "Head-On")
                           Severity_Level VARCHAR(50), -- Severity level of the crash (e.g., "Minor", "Severe")
                           Light_Conditions VARCHAR(50), -- Lighting conditions during the crash (e.g., "Daylight")
                           Road_Conditions VARCHAR(50), -- Road surface conditions (e.g., "Dry", "Wet")
                           Traffic_Control VARCHAR(50), -- Traffic control present (e.g., "Stop Sign", "Traffic Signal")
                           Is_Hit_And_Run BIT -- Indicates if the crash was a hit-and-run (1 for yes, 0 for no)
);
CREATE TABLE Person_Dim (
                            Person_ID INT PRIMARY KEY, -- Unique identifier for the person
                            Age INT, -- Age of the person
                            Gender VARCHAR(10), -- Gender of the person (e.g., "Male", "Female")
                            Role VARCHAR(50), -- Role in the accident (e.g., "Driver", "Passenger", "Pedestrian")
                            Injury_Level VARCHAR(50), -- Level of injury (e.g., "None", "Severe")
                            Is_Impaired BIT, -- Indicates if the person was impaired by drugs/alcohol (1 for yes, 0 for no)
                            License_Status VARCHAR(50), -- Driver's license status (e.g., "Valid", "Suspended")
                            Is_Resident BIT -- Indicates if the person is a local resident (1 for yes, 0 for no)
);
CREATE TABLE Weather_Dim (
                             Weather_ID INT PRIMARY KEY, -- Unique identifier for the weather condition
                             Condition VARCHAR(50), -- Weather condition (e.g., "Clear", "Rain", "Snow")
                             Temperature DECIMAL(5,2), -- Temperature in degrees Celsius
                             Visibility INT, -- Visibility in meters
                             Wind_Speed DECIMAL(5,2), -- Wind speed in km/h
                             Precipitation DECIMAL(5,2), -- Precipitation amount in mm
                             Humidity INT -- Humidity percentage
);
CREATE TABLE Cause_Dim (
                           Cause_ID INT PRIMARY KEY, -- Unique identifier for the cause
                           Cause_Type VARCHAR(255), -- Type of cause (e.g., "Speeding", "Distracted Driving")
                           Is_Alcohol_Related BIT, -- Indicates if alcohol was involved (1 for yes, 0 for no)
                           Is_Drug_Related BIT -- Indicates if drugs were involved (1 for yes, 0 for no)
);
CREATE TABLE Road_Dim (
                          Road_ID INT PRIMARY KEY, -- Unique identifier for the road
                          Road_Name VARCHAR(255), -- Name of the road
                          Road_Type VARCHAR(50), -- Type of road (e.g., "Highway", "Urban")
                          Speed_Limit INT, -- Speed limit on the road (in km/h)
                          Lane_Count INT, -- Number of lanes on the road
                          Is_Toll_Road BIT -- Indicates if the road is a toll road (1 for yes, 0 for no)
);
CREATE TABLE Driver_Behavior_Dim (
                                     Behavior_ID INT PRIMARY KEY, -- Unique identifier for the driver behavior
                                     Is_Speeding BIT, -- Indicates if the driver was speeding (1 for yes, 0 for no)
                                     Is_Distracted BIT, -- Indicates if the driver was distracted (1 for yes, 0 for no)
                                     Is_Fatigue BIT -- Indicates if the driver was fatigued (1 for yes, 0 for no)
);
CREATE TABLE Damage_Fact (
                             Damage_ID INT PRIMARY KEY, -- Unique identifier for the fact table
                             Date_ID INT, -- Foreign key to Date_Dim
                             Vehicle_ID INT, -- Foreign key to Vehicle_Dim
                             Location_ID INT, -- Foreign key to Geography_Dim
                             Crash_ID INT, -- Foreign key to Crash_Dim
                             Person_ID INT, -- Foreign key to Person_Dim
                             Weather_ID INT, -- Foreign key to Weather_Dim
                             Cause_ID INT, -- Foreign key to Cause_Dim
                             Road_ID INT, -- Foreign key to Road_Dim
                             Driver_Behavior_ID INT, -- Foreign key to Driver_Behavior_Dim
                             Damage_Cost DECIMAL(18,2), -- Total damage cost in dollars
                             Num_Units INT, -- Number of units involved (people/vehicles)
                             FOREIGN KEY (Date_ID) REFERENCES Date_Dim(Date_ID),
                             FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle_Dim(Vehicle_ID),
                             FOREIGN KEY (Location_ID) REFERENCES Geography_Dim(Location_ID),
                             FOREIGN KEY (Crash_ID) REFERENCES Crash_Dim(Crash_ID),
                             FOREIGN KEY (Person_ID) REFERENCES Person_Dim(Person_ID),
                             FOREIGN KEY (Weather_ID) REFERENCES Weather_Dim(Weather_ID),
                             FOREIGN KEY (Cause_ID) REFERENCES Cause_Dim(Cause_ID),
                             FOREIGN KEY (Road_ID) REFERENCES Road_Dim(Road_ID),
                             FOREIGN KEY (Driver_Behavior_ID) REFERENCES Driver_Behavior_Dim(Behavior_ID)
);