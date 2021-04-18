import re
import calendar
from datetime import datetime


class Validator:
    """Class for JSON data validation after POST/PUT request"""

    REQUIRED_FIELDS = [
        'title',
        'start_date',
        'end_date',
        'lectures_number'
    ]

    def __init__(self, data):
        self.data = data
        self.errors = {}

    def validate_required_fields(self) -> None:
        for field in self.REQUIRED_FIELDS:
            if not self.data.get(field, ''):
                self.errors[field] = f'"{field}" is required field'

    def check_date_string_format(self, data: str, date_name: str) -> bool:
        """
        Check if date in format 'dd/mm/yyyy'
        :param data: str
        :param date_name: str
        :return: bool
        """
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
            self.errors[f'{date_name}'] = f'Input "{date_name}" as dd/mm/yyyy'
            return False
        return True

    def check_if_date_exists(self, date: str, date_name: str) -> bool:
        """
        Check days, months number, if inputted year not less then current year
        :param date: date as string in format 'dd/mm/yyyy'
        :param date_name: date's name
        :return: bool
        """
        if self.check_date_string_format(date, date_name):
            day, month, year = map(int, date.split('/'))
            day_limit = calendar.monthrange(year, month)[1]
            current_year = int(datetime.now().strftime('%Y'))
            if 0 < day <= day_limit and 0 < month < 13 and year >= current_year - 1:
                return True
            else:
                self.errors[f'{date_name}'] = f'"{date_name}" is not exists or in the past'
                return False

    @staticmethod
    def str_to_datetime(date_as_str: str) -> datetime:
        return datetime.strptime(date_as_str, '%d/%m/%Y')

    def validate_date_chronology(self) -> bool:
        """
        Check if start_date less then end_date
        :return: bool
        """
        start_date = self.data.get('start_date', '')
        end_date = self.data.get('end_date', '')
        if self.check_if_date_exists(start_date, 'start_date') and self.check_if_date_exists(end_date, 'end_date'):
            if self.str_to_datetime(end_date) < self.str_to_datetime(start_date):
                self.errors['start_date'] = '"start_date" mast be earlier then "end_date"'
                return False
            return True

    def validate_lectures_number(self) -> None:
        """
        Check if lectures_number is digit
        :return: bool
        """
        lectures_number = self.data.get('lectures_number', '')
        if isinstance(lectures_number, str):
            if not lectures_number.isdigit():
                self.errors['lectures_number'] = 'Must be a digit'

    def validate_title_length(self) -> None:
        """
        Check title length
        :return: bool
        """
        if len(self.data.get('title', '')) > 128:
            self.errors['wrong_title_length'] = 'Must be less then 128'

    def check_errors(self) -> dict:
        """
        Run all validators and collect errors
        :return: errors dict
        """
        self.validate_required_fields()
        self.validate_date_chronology()
        self.validate_title_length()
        self.validate_lectures_number()
        return self.errors
