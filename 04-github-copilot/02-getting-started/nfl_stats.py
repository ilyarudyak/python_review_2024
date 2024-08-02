import csv

# Open the CSV file
with open('nfl_offensive_stats.csv', 'r') as file:
    # Read the CSV data
    csv_data = csv.reader(file)
    # Initialize the sum of yards
    passing_yards = 0

    # Iterate over each row in the CSV data
    for row in csv_data:
        # Check if the player is "Aaron Rodgers"
        if row[3] == "Aaron Rodgers":
            # Add the passing yards to the sum
            passing_yards += int(row[7])

    # Print the sum of yards
    print(f"Total passing yards for Aaron Rodgers: {passing_yards}")