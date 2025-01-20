import csv

# Path to the dataset
fact_table_path = '/Users/elvislleshi/Desktop/LDS24_straordinario - Data/fact_cleaned.csv'

# Read the dataset and check for NaN values
nan_counts = {}
total_rows = 0

cleaned_rows = []

with open(fact_table_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # Read the header
    headers = next(csv_reader)
    nan_counts = {header: 0 for header in headers}  # Initialize counters for NaN values

    # Iterate through rows
    for row in csv_reader:
        total_rows += 1
        for i, value in enumerate(row):
            if value == "" or value.lower() == "nan":  # Check for empty or 'nan' values
                nan_counts[headers[i]] += 1

        # Filter rows where winner_ioc or loser_ioc are empty
        if row[headers.index("winner_ioc")].strip() and row[headers.index("loser_ioc")].strip():
            cleaned_rows.append(row)

# Display the NaN counts for each column
print("Total Rows:", total_rows)
print("NaN Values per Column:")
for column, count in nan_counts.items():
    print(f"{column}: {count}")

# Save the cleaned dataset to a new file
cleaned_file_path = '/Users/elvislleshi/Desktop/LDS24_straordinario - Data/fact_cleaned_no_nan.csv'
with open(cleaned_file_path, mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    # Write the header
    csv_writer.writerow(headers)

    # Write the cleaned rows
    csv_writer.writerows(cleaned_rows)

print(f"Cleaned dataset saved to {cleaned_file_path}")
