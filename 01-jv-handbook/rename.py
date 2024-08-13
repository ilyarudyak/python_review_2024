import os

# Specify the directory containing the files
directory = '.'

# List all files in the directory
files = os.listdir(directory)

# Iterate through the files and rename them
for filename in files:
    if filename.startswith('ch'):
        new_filename = filename[2:]  # Remove the first two characters
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

