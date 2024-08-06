import unittest
from log_parser.log_parser_v2 import LogParser

class LogParserTests(unittest.TestCase):
    def test_get_parsed_log(self):
        log_parser = LogParser('log_parser/log_file.log')
        log_parser.parse_file()

        parsed_log = log_parser.get_parsed_log()

        self.assertIsInstance(parsed_log, list)
        self.assertEqual(len(parsed_log), 5)
        self.assertEqual(parsed_log[0]['timestamp'], '2024-08-05 10:15:30')
        self.assertEqual(parsed_log[0]['type'], 'USER')
        self.assertEqual(parsed_log[0]['user'], 'john_doe')
        self.assertEqual(parsed_log[0]['message'], 'Logged in successfully')
        self.assertEqual(parsed_log[1]['timestamp'], '2024-08-05 10:16:45')
        self.assertEqual(parsed_log[1]['type'], 'SYSTEM')
        self.assertEqual(parsed_log[1]['message'], 'BACKUP - Daily backup completed')
        self.assertEqual(parsed_log[2]['timestamp'], '2024-08-05 10:17:20')
        self.assertEqual(parsed_log[2]['type'], 'ERROR')
        self.assertEqual(parsed_log[2]['error_code'], '404')
        self.assertEqual(parsed_log[2]['message'], 'Page not found')
        self.assertEqual(parsed_log[3]['timestamp'], '2024-08-05 10:18:00')
        self.assertEqual(parsed_log[3]['type'], 'USER')
        self.assertEqual(parsed_log[3]['user'], 'jane_smith')
        self.assertEqual(parsed_log[3]['message'], "Uploaded file 'document.pdf'")
        self.assertEqual(parsed_log[4]['timestamp'], '2024-08-05 10:19:15')
        self.assertEqual(parsed_log[4]['type'], 'SYSTEM')
        self.assertEqual(parsed_log[4]['message'], 'UPDATE - System updated to version 2.1')

if __name__ == '__main__':
    unittest.main()