import pyodbc

# Connection parameters
server = 'tcp:lds.di.unipi.it'  # Specified server
username = 'Group_ID_10'        # Username
password = 'FRU5YM7A'           # Password
database = 'Group_ID_10_DB'     # Database name

# Building the connection string
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    # Connecting to the database
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()

    # Query to fetch data
    query = "SELECT TOP 10 * FROM Cause_Dim"
    cursor.execute(query)

    # Fetching data and displaying the 'Cause_Type' column
    print("Cause_ID | Cause_Type")
    print("----------------------")
    for row in cursor.fetchall():
        print(f"{row.Cause_ID} | {row.Cause_Type}")

except Exception as e:
    print(f"Error during query execution: {e}")

finally:
    # Cleaning up resources
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnxn' in locals() and cnxn:
        cnxn.close()
