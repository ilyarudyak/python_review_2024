import re
import logging

class LogParser:
    """
    Objective: Write a Python function that parses a log file and extracts specific 
    information from each log entry. The log file contains entries with varying formats, 
    and you need to extract and categorize the information.

    Description:
    - Your function should take a string (the contents of the log file) as input.
    - It should return a list of dictionaries, where each dictionary represents a parsed log entry.
    - The log entries can be in one of the following formats:
        1) [TIMESTAMP] USER: MESSAGE
        2) [TIMESTAMP] SYSTEM: ACTION - DETAILS
        3) [TIMESTAMP] ERROR (CODE): ERROR_MESSAGE
    - The timestamp format is always YYYY-MM-DD HH:MM:SS
    - Extract the following information for each log entry:
        - Timestamp
        - Type (USER, SYSTEM, or ERROR)
        - User name (for USER type)
        - Message (for USER type)
        - Action and Details (for SYSTEM type)
        - Error Code and Error Message (for ERROR type)

    Example Input:
    [2024-08-05 10:15:30] USER: john_doe: Logged in successfully
    [2024-08-05 10:16:45] SYSTEM: BACKUP - Daily backup completed
    [2024-08-05 10:17:20] ERROR (404): Page not found
    [2024-08-05 10:18:00] USER: jane_smith: Uploaded file 'document.pdf'
    [2024-08-05 10:19:15] SYSTEM: UPDATE - System updated to version 2.1

    """
    
    # Log keys
    TIMESTAMP = 'timestamp'
    TYPE = 'type'
    USER = 'user'
    MESSAGE = 'message'
    ERROR_CODE = 'error_code'
    USERNAME = 'username'
    
    # Log types
    TYPE_USER = 'USER'
    TYPE_SYSTEM = 'SYSTEM'
    TYPE_ERROR = 'ERROR'
    
    def __init__(self, file_name):
        self._parsed_log = []
        self._file_name = file_name

        # Regex pattern
        self.log_pattern = re.compile(r'''
            \[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]  # Timestamp
            \s+
            (?P<type>USER|SYSTEM|ERROR)                              # Log type
            (?:\s+\((?P<error_code>\d+)\))?:                         # Optional error code for ERROR type
            \s+
            ((?P<username>\w+):)?                                    # Optional username for USER type
            (?P<message>.+)                                          # Message content
        ''', re.VERBOSE)

    def get_parsed_log(self):
        """
        Return the parsed log entries.
        """

        return self._parsed_log

    def parse_file(self):
        """ 
        Parse the log file and extract log entries 
        with timestamp, type, username, error code, and message.
        """
        try:
            with open(self._file_name) as file:
                for line in file:
                    self._parse_line(line)
        except IOError as e:
            logging.error(f"Error reading file: {e}")

    def _parse_line(self, line):
        """ 
        Parse a single line from the log file 
        and extract the timestamp, type, username, error code, and message.
        """

        # Create a new dictionary to store the parsed line
        parsed_line = {}

        # Match the log pattern
        match = self.log_pattern.match(line)
        if match:
            parsed_line = {
                self.TIMESTAMP: match.group(self.TIMESTAMP),
                self.TYPE: match.group(self.TYPE),
                self.MESSAGE: match.group(self.MESSAGE).strip()
            }
            # Extract optional fields
            if match.group(self.USERNAME):
                parsed_line[self.USER] = match.group(self.USERNAME)
            if match.group(self.ERROR_CODE):
                parsed_line[self.ERROR_CODE] = match.group(self.ERROR_CODE)
            self._parsed_log.append(parsed_line)

        else:
            logging.warning(f"Failed to parse line: {line.strip()}")


if __name__ == '__main__':
    log_parser = LogParser('log_parser/log_file.log')
    log_parser.parse_file()
    for parsed_line in log_parser._parsed_log:
        print(parsed_line)