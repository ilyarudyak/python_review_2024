import re

class LogParser:
    
    def __init__(self, file_name) -> None:
        self.log = []
        self.file_name = file_name
        # Log keys
        self.TIMESTAMP = 'timestamp'
        self.TYPE = 'type'
        self.USER = 'user'
        self.MESSAGE = 'message'
        self.ERROR_CODE = 'error_code'
        # Types
        self.TYPE_USER = 'USER'
        self.TYPE_SYSTEM = 'SYSTEM'
        self.TYPE_ERROR = 'ERROR'
        # Regex patterns
        self.timestamp_pattern = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]')
        self.type_pattern = re.compile(r'\]\s+([\w]+)\s?\(?(\d{0,3})\)?:')
        self.user_pattern = re.compile(r'USER:\s+(\w+):')
        self.message_pattern = re.compile(r':\s+([\w\d.\s\'-]+)\n')

    def parse_file(self):
        with open(self.file_name) as file:
            for line in file:
                self._parse_line(line)

    # Utility methods
    def _parse_line(self, line):

        # Create a new dictionary to store the parsed line
        parsed_line = {}

        # 1 - Extract timespamp
        timestamp = self._extract_timestamp(line)
        if timestamp:
            parsed_line[self.TIMESTAMP] = timestamp

        # 2 - Extract type
        type = self._extract_type(line)
        if type:
            parsed_line[self.TYPE] = type

        if type == self.TYPE_USER:
            # 3.1 Extract user
            user = self._extract_user(line)
            if user:
                parsed_line[self.USER] = user

        elif type == self.TYPE_SYSTEM:
            pass

        elif type == self.TYPE_ERROR:
            # 3.3 - Extract error code
            error_code = self._extract_error_code(line)
            if error_code:
                parsed_line[self.ERROR_CODE] = error_code

        else:
            raise ValueError(f"Unknown type: {type}")
        
        # 4 - Extract message
        message = self._extract_message(line)
        if message:
            parsed_line[self.MESSAGE] = message

        # Append the parsed line to the log
        self.log.append(parsed_line)

    def _extract_timestamp(self, line):
        match = self.timestamp_pattern.match(line)
        if match:
            return match.group(1)    
        return None
    
    def _extract_type(self, line):
        match = self.type_pattern.search(line)
        if match:
            type = match.group(1)
            return type    
        return None
    
    def _extract_error_code(self, line):
        match = self.type_pattern.search(line)
        if match:
            error_code = match.group(2)
            return error_code    
        return None
    
    def _extract_user(self, line):      
        match = self.user_pattern.search(line)
        if match:
            return match.group(1)    
        return None
    
    def _extract_message(self, line):
        match = self.message_pattern.search(line)
        if match:
            return match.group(1).rstrip()    
        return None
    

if __name__ == '__main__':
    log_parser = LogParser('log_file.log')
    log_parser.parse_file()
    for parsed_line in log_parser.log:
        print(parsed_line)