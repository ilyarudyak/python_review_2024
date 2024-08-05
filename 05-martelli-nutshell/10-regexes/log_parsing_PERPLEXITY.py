import re
from typing import List, Dict, Tuple, Optional

class LogParser:
    def __init__(self, file_name: str) -> None:
        self.log: List[Dict[str, str]] = []
        self.file_name = file_name
        # Log keys
        self.TIMESTAMP = 'timestamp'
        self.TYPE = 'type'
        self.USER = 'user'
        self.MESSAGE = 'message'
        self.ERROR_CODE = 'error_code'
        self.ACTION = 'action'
        self.DETAILS = 'details'
        # Types
        self.TYPE_USER = 'USER'
        self.TYPE_SYSTEM = 'SYSTEM'
        self.TYPE_ERROR = 'ERROR'
        # Regex patterns
        self.timestamp_pattern = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]')
        self.type_pattern = re.compile(r'\]\s+([\w]+)\s?\(?(\d{0,3})\)?:')
        self.user_pattern = re.compile(r'USER:\s+(\w+):')
        self.message_pattern = re.compile(r':\s+(.+)$')
        self.system_pattern = re.compile(r'SYSTEM:\s+(\w+)\s+-\s+(.+)$')

    def parse_file(self) -> None:
        """Parse the log file and store the results."""
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    self._parse_line(line.strip())
        except IOError as e:
            print(f"Error reading file: {e}")

    def _parse_line(self, line: str) -> None:
        """Parse a single line of the log file."""
        parsed_line = {}
        
        timestamp = self._extract_timestamp(line)
        type_ = self._extract_type(line)
        
        if timestamp and type_:
            parsed_line[self.TIMESTAMP] = timestamp
            parsed_line[self.TYPE] = type_

            if type_ == self.TYPE_USER:
                user = self._extract_user(line)
                message = self._extract_message(line)
                if user:
                    parsed_line[self.USER] = user
                if message:
                    parsed_line[self.MESSAGE] = message
            elif type_ == self.TYPE_SYSTEM:
                action, details = self._extract_system_info(line)
                if action:
                    parsed_line[self.ACTION] = action
                if details:
                    parsed_line[self.DETAILS] = details
            elif type_ == self.TYPE_ERROR:
                error_code = self._extract_error_code(line)
                message = self._extract_message(line)
                if error_code:
                    parsed_line[self.ERROR_CODE] = error_code
                if message:
                    parsed_line[self.MESSAGE] = message
            else:
                print(f"Unknown log type: {type_}")

            self.log.append(parsed_line)

    def _extract_timestamp(self, line: str) -> Optional[str]:
        match = self.timestamp_pattern.match(line)
        return match.group(1) if match else None

    def _extract_type(self, line: str) -> Optional[str]:
        match = self.type_pattern.search(line)
        return match.group(1) if match else None

    def _extract_error_code(self, line: str) -> Optional[str]:
        match = self.type_pattern.search(line)
        return match.group(2) if match and match.group(2) else None

    def _extract_user(self, line: str) -> Optional[str]:
        match = self.user_pattern.search(line)
        return match.group(1) if match else None

    def _extract_message(self, line: str) -> Optional[str]:
        match = self.message_pattern.search(line)
        return match.group(1).strip() if match else None

    def _extract_system_info(self, line: str) -> Tuple[Optional[str], Optional[str]]:
        match = self.system_pattern.search(line)
        return (match.group(1), match.group(2)) if match else (None, None)
    
if __name__ == '__main__':
    log_parser = LogParser('log_file.log')
    log_parser.parse_file()
    for parsed_line in log_parser.log:
        print(parsed_line)