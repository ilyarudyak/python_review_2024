import re

if __name__ == '__main__':

    TIMESTAMP = 'timestamp'

    # Define a regex pattern with named groups and conditional extraction
    log_pattern = re.compile(r'''
        \[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # Timestamp
        \s+
        (?P<type>USER|SYSTEM|ERROR)  # Log type
        (?:
            \s+\((?P<error_code>\d+)\)  # Optional error code for ERROR type
        )?:
        \s+
        ((?P<username>\w+):)?
        (?P<message>.+)  # Message content
    ''', re.VERBOSE)

    # Example log entries
    log_entries = [
        "[2024-08-05 10:15:30] USER: john_doe: Logged in successfully",
        "[2024-08-05 10:16:45] SYSTEM: BACKUP - Daily backup completed",
        "[2024-08-05 10:17:20] ERROR (404): Page not found",
        "[2024-08-05 10:18:00] USER: jane_smith: Uploaded file 'document.pdf'"
    ]

    # Parse log entries
    for entry in log_entries:
        match = log_pattern.match(entry)
        if match:
            print("Parsed log entry:")
            print(f"  Timestamp: {match.group('timestamp')}")
            print(f"  Type: {match.group('type')}")
            if match.group('username'):
                print(f"  Username: {match.group('username')}")
            if match.group('error_code'):
                print(f"  Error Code: {match.group('error_code')}")
            print(f"  Message: {match.group('message').strip()}")
            print()