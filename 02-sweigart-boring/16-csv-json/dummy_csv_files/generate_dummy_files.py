import os

# Function to generate files
def generate_files():
    for i in range(1, 11):
        filename = f"NAICS_data_{i:02}.csv"
        with open(filename, 'w') as f:
            f.write("Filename,Line\n")
            for j in range(1, 6):
                f.write(f"{filename},line {j}\n")
        print(f"Generated {filename}")

# Run the function
if __name__ == "__main__":
    generate_files()