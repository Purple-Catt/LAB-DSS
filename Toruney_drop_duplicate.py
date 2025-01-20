import csv

# Path to the dataset
fact_table_path = '/Users/elvislleshi/Desktop/LDS24_straordinario - Data/tourney_cleaned.csv'

# Read the CSV file and remove rows with identical values across all columns
with open(fact_table_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # Read the header
    headers = next(csv_reader)

    # Use a set to track unique rows
    unique_rows = set()
    cleaned_rows = []

    for row in csv_reader:
        # Convert the row to a tuple (hashable) to add to the set
        row_tuple = tuple(row)
        if row_tuple not in unique_rows:
            unique_rows.add(row_tuple)
            cleaned_rows.append(row)  # Only add unique rows to the result

# Save the cleaned dataset to a new file
cleaned_file_path = '/Users/elvislleshi/Desktop/LDS24_straordinario - Data/tourney_cleaned_cleaned.csv'
with open(cleaned_file_path, mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    # Write the header
    csv_writer.writerow(headers)

    # Write the cleaned rows
    csv_writer.writerows(cleaned_rows)

print(f"Cleaned dataset saved to {cleaned_file_path}")
