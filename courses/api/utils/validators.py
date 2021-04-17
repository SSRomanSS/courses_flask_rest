import re
from datetime import datetime


class Validator:

    REQUIRED_FIELDS = [
        'title',
        'start_date',
        'end_date',
        'lectures_number'
    ]

    def __init__(self, data):
        self.data = data
        self.errors = {}

    def _validate_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if not self.data.get(field, ''):
                self.errors[field] = f'{field} is required'

    def _check_date_string_format(self, data):
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', data):
            self.errors['wrong_date_format'] = 'input date as dd/mm/yyyy'
            return False
        return True

    def check_date_range_format(self, date):
        if self._check_date_string_format(date):
            day, month, year = date.split('/')
            # TODO add check February
            if 0 < int(day) < 32 and 0 < int(month) < 13 and int(year) >= 2021:
                return True
            else:
                self.errors['wrong_date_range'] = 'wrong date range'
                return False

    @staticmethod
    def str_to_datetime(date_as_str: str) -> datetime:
        return datetime.strptime(date_as_str, '%d/%m/%Y')

    def _validate_date_chronology(self):
        start_date = self.data.get('start_date', '')
        end_date = self.data.get('end_date', '')
        if self.check_date_range_format(start_date) and self.check_date_range_format(end_date):
            if self.str_to_datetime(end_date) < self.str_to_datetime(start_date):
                self.errors['wrong_date_chronology'] = 'start_date mast be earlier then end_date'

    def _validate_lectures_number(self):
        lectures_number = self.data.get('lectures_number', '')
        if isinstance(lectures_number, str):
            if not lectures_number.isdigit():
                self.errors['wrong_lectures_number'] = 'must be a digit'

    def _validate_title_length(self):
        if len(self.data.get('title', '')) > 128:
            self.errors['wrong_title_length'] = 'must be less then 128'

    def check_errors(self):
        self._validate_required_fields()
        self._validate_date_chronology()
        self._validate_title_length()
        self._validate_lectures_number()
        return self.errors
