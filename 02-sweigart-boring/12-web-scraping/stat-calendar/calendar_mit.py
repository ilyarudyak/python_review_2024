import re
import datetime
from collections import defaultdict
from datetime_utils import get_datetime_from_string

class CalendarScraper:
    """
    The goal of this class is to parse a calendar for the course MITx 18.6501x
    Fundamentals of Statistics on EDX: https://learning.edx.org/course/course-v1:MITx+18.6501x+2T2024/dates

    We need to extract the following information:
    - Due dates for each Lecture Exercises;
    - Due dates for each Homework;
    - Due dates for Midterm and Final Exam;

    We will parse the text file with all these due dates (parsing web directly is not allowed).
    We will be using regex to extract the information.
    """
    
    def __init__(self, file_path='calendar_mit.txt'):
        self.file_path = file_path
        self._exercises = defaultdict(list)
        self._homeworks = defaultdict(list)
        self._exams = {}
        self._date = None

    def get_calendar(self):
        """
        Parses the calendar file and extracts the due dates for the exercises, homeworks and exams.
        """
        with open(self.file_path, 'r') as file:
            for lines in file.read().split('-----'):
                for line in lines.split('\n'):
                    if line.startswith('Wed') or line.startswith('Mon'):
                        self._get_date(line)
                    elif line.startswith('Exercises'):
                        self._get_exercise(line)
                    elif line.startswith('Homework'):
                        self._get_homework(line)
                    elif line.startswith('Midterm') or line.startswith('Final'):
                        self._get_exam(line)
                    else:
                        continue

    def _get_date(self, line):
        """
        Extracts the date from a line.
        Wed, Sep 4, 2024
        Mon, Nov 25, 2024
        """
        date_pattern = re.compile(r"""
            (?P<day_name>\w{3}),
            \s+
            (?P<month>\w{3})
            \s+
            (?P<day>\d{1,2}),
            \s+
            (?P<year>\d{4})
        """, 
        re.VERBOSE | re.IGNORECASE)
        date = date_pattern.search(line)
        if date:
            date_str = date.group(0).strip() + ' 11:59 AM UTC'
            dt = get_datetime_from_string(date_str)
            self._date = dt.ctime()

    def _get_exercise(self, line):
        """
        Extracts the due date of the lecture exercise.
        Exercises: Lecture 1: What is statistics due 11:59 AM UTC
        """
        exercise_pattern = re.compile(r"""
            Exercises:
            \s+
            Lecture\s+(?P<lecture_number>\d{1,2}):
            \s+
            (?P<lecture_title>[\s\w;:\-]+)
            due
            """, 
            re.VERBOSE | re.IGNORECASE)
        
        exercise_match = exercise_pattern.search(line)
        if exercise_match:
            lecture = f"Lecture {int(exercise_match.group('lecture_number')):02d}: {exercise_match.group('lecture_title').strip()}"
            self._exercises[self._date].append(lecture)

    def _get_homework(self, line):
        """
        Extracts the due date of the homework.
        Homework: Homework 0: Probability Review, Modes of Convergence and Optional Linear Algebra Exercises due 11:59 AM UTC
        """
        homework_pattern = re.compile(r"""
            Homework:\s+                
            Homework\s+(?P<homework_number>\d{1,2})
            \s*
            (?P<homework_title>[\s\w,;:()\-]*)?
            due
            """, 
            re.VERBOSE | re.IGNORECASE)
        
        homework_match = homework_pattern.search(line)
        if homework_match:
            homework = f"Homework {int(homework_match.group('homework_number')):02d}"
            if homework_match.group('homework_title'):
                homework += f": {homework_match.group('homework_title').strip()}"
            self._homeworks[self._date].append(homework)

    def _get_exam(self, line):
        """
        Extracts the due date of the exam.
        Midterm: Midterm Exam due 11:59 AM UTC
        Final: Final Exam due 11:59 AM UTC
        """
        exam_pattern = re.compile(r"""
            (?P<exam_type>Midterm|Final):
            \s+
            (?P<exam_title>[\s\w]+)
            due
            """, 
            re.VERBOSE | re.IGNORECASE)
        
        exam_match = exam_pattern.search(line)
        if exam_match.group('exam_title'):
            exam = f"{exam_match.group('exam_title').strip()}"
            self._exams[self._date] = exam
    
    def _get_num_exercices(self):
        num_dates = len(self._exercises)
        num_exercices = sum([len(exercices) for exercices in self._exercises.values()])
        return num_dates, num_exercices
    
    def _get_num_homeworks(self):
        num_dates = len(self._homeworks)
        num_homeworks = sum([len(homeworks) for homeworks in self._homeworks.values()])
        return num_dates, num_homeworks


if __name__ == '__main__':
    cs = CalendarScraper()
    cs.get_calendar()
    print(cs._get_num_exercices())
    print(cs._get_num_homeworks())
    print(cs._exams)