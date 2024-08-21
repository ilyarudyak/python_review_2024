import re
import json
from pathlib import Path

class RobocopyLogParser:
    """
    A class to parse a Robocopy log file. 
    
    It extracts the following information:
    - Source and destination directory from the header section of the log file.
    - Metric data from the summary section of the log file: directories, files
      and bytes copied.
    - Error information from the summary section of the log file in case the logging 
      was unsuccessfull.

    It defines 3 regular expressions to match this information in the log file. Extracted 
    information is stored in a json file. There's one json file for each log file.
    """
    # Patterns to match the source and destination directory, error and metrics data
    PATTERN_DIRECTORY = re.compile(r'''
        ^\s+
        (?P<type>Source|Dest)              # Source or Destination directory
        \s+:\s+
        (?P<dir>.+)$                       # Directory path
        ''',                                   
        re.VERBOSE | re.IGNORECASE)
    PATTERN_ERROR = re.compile(r'''^(?P<error_message>.*error.*)$''', re.IGNORECASE)
    PATTERN_METRICS = re.compile(r'''
        ^\s*
        (?P<type>Dirs|Files|Bytes)  # Directories, files or bytes
        \s+:\s+
        (?P<total>\d+)                       # Total
        \s+
        (?P<copied>\d+)                      # Copied
        \s+
        (?P<skipped>\d+)                     # Skipped
        \s+
        (?P<mismatch>\d+)                    # Mismatch
        \s+
        (?P<failed>\d+)                      # Failed
        \s+
        (?P<extras>.*)                       # Extras
        ''', 
        re.VERBOSE | re.IGNORECASE)

    # Constants for the json file keys
    TYPE = 'type'
    DIR = 'dir'
    ERROR = 'error'
    ERROR_MESSAGE = 'error_message'

    LOG_FILE = 'log_file_name'
    DIRECTORY = 'directory'
    METRICS = 'metrics'

    def __init__(self, log_files):
        self.log_files = log_files
        # source and destionation directory paths 
        self.directory = {}
        # list of dictionaries, one dictionary per metrics data: 
        # directories, files and bytes copied                 
        self.metrics = []; 
        self.error = False  
        self.error_message = ''

    def _reset(self):
        """
        Reset the instance variables.
        """
        self.directory = {}
        self.metrics = []
        self.error = False
        self.error_message = '' 

    def parse_log_files(self):
        """
        Parse the log files and store the information in json files.
        """
        for log_file in self.log_files:
            self._parse_log_file(log_file)
            self._serialize_to_json(log_file)
            self._reset()

    def _parse_log_file(self, log_file):
        """
        Parse a log file and store the information in a json file.
        """
        with open(log_file) as file:
            for line in file:
                self._parse_line(line)

            # print(self.directory, self.metrics, self.error, self.error_message)

    def _parse_line(self, line):

        directory_match = self.PATTERN_DIRECTORY.search(line)
        if directory_match:
            self.directory[directory_match.group(self.TYPE)] = directory_match.group(self.DIR)

        error_match = self.PATTERN_ERROR.search(line)
        if error_match:
            self.error = True
            self.error_message = error_match.group(self.ERROR_MESSAGE)

        metrics_match = self.PATTERN_METRICS.search(line)
        if metrics_match:
            metrics_row = {}
            for key,value in metrics_match.groupdict().items():
                if key == self.TYPE:
                    metrics_row[key] = value
                else:
                    metrics_row[key] = int(value)               
            self.metrics.append(metrics_row)
             
    def _get_json_file_name(self, log_file):
        """
        Return the json file name for a log file.
        """
        return Path(log_file).with_suffix('.json')
    
    def _serialize_to_json(self, log_file):
        """
        Serialize the instance variables to a json file.
        """
        data = {
            self.LOG_FILE: log_file,
            self.DIRECTORY: self.directory,
            self.METRICS: self.metrics,
            self.ERROR: self.error,
            self.ERROR_MESSAGE: self.error_message
        }
        json_file = self._get_json_file_name(log_file)
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)

if __name__ == '__main__':
    log_files = ['robocopy.log', 'robocopy_invalid_source.log']
    parser = RobocopyLogParser(log_files)
    parser.parse_log_files()
