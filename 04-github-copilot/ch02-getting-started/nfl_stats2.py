import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Specify the path to the CSV file
csv_file_path = "nfl_offensive_stats.csv"

# Open the CSV file
with open(csv_file_path, "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Create a defaultdict to store players and their sum of yards
    passing_yards = defaultdict(int)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Check if the position is "QB"
        if row[2] == "QB":
            # Get the player name and yards
            player = row[3]
            yards = int(row[7])
            
            # Add the yards to the player's sum
            passing_yards[player] += yards

    # Print the players and their sum of yards
    # Sort the players by sum of yards in descending order
    sorted_passing_yards = sorted(passing_yards.items(), key=lambda x: x[1], reverse=True)

    # Print the players and their sum of yards in descending order
    for player, yards in sorted_passing_yards[:10]:
        if player != "Tom Brady":
            print(f"{player}: {yards}")

    # Filter players with more than 10000 passing yards
    filtered_players = [(player, yards) for player, yards in sorted_passing_yards if yards > 10000]

    # Extract player names and passing yards
    players = [player for player, _ in filtered_players]
    yards = [yards for _, yards in filtered_players]

    # Plot the players by their number of passing yards
    plt.bar(players, yards)
    plt.xlabel("Player")
    plt.ylabel("Passing Yards")
    plt.title("Players with More Than 10000 Passing Yards")
    plt.xticks(rotation=90)
    plt.show()



