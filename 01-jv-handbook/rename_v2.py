import os
import re

# Specify the directory containing the files
directory = '.'

# List all files in the directory
files = os.listdir(directory)

# Define the regex pattern to match the file names
pattern = r'^(\d)-'

# Iterate through the files and rename them
for filename in files:
    match = re.match(pattern, filename)
    if match:
        new_filename = re.sub(pattern, r'0\1-', filename)  # Add a leading '0'
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

