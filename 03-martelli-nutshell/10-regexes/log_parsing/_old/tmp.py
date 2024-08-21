import re

if __name__ == '__main__':

    # Define the regex pattern
    pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'

    # Compile the regex pattern
    compiled_pattern = re.compile(pattern)

    # Test string
    test_string = "[2024-08-05 10:15:30]"

    # Match the pattern
    match = compiled_pattern.match(test_string)
    if match:
        print("Match found:", match.group())
    else:
        print("No match found")