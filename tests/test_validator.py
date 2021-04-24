from datetime import datetime
import unittest
from courses.api.services import Validator


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.correct_data = {
            'title': 'Title',
            'start_date': '01/01/2022',
            'end_date': '01/05/2022',
            'lectures_number': '10',
        }
        self.incorrect_data = {
            'start_date': '01.01.2022',
            'end_date': '45/05/2022',
            'lectures_number': 'two',
        }
        self.incorrect_data_date_reverse = {
            'start_date': '01/01/2023',
            'end_date': '01/05/2022',
        }
        self.empty_data = {}

    def test_validate_required_fields(self):
        validator1 = Validator(self.correct_data)
        validator2 = Validator(self.empty_data)
        validator1.validate_required_fields()
        self.assertFalse(validator1.errors)
        validator2.validate_required_fields()
        self.assertDictEqual(
            {key: f'"{key}" is required field' for key in self.correct_data},
            validator2.errors
        )

    def test_check_date_string_format(self):
        validator1 = Validator(self.incorrect_data)
        validator2 = Validator(self.correct_data)
        self.assertFalse(validator1.check_date_string_format(self.incorrect_data['start_date'], 'start_date'))
        self.assertEqual('Input "start_date" as dd/mm/yyyy',
                         validator1.errors['start_date'])
        self.assertTrue(validator2.check_date_string_format(self.correct_data['start_date'], 'start_date'))

    def test_check_if_date_exists(self):
        validator1 = Validator(self.incorrect_data)
        validator2 = Validator(self.correct_data)
        self.assertFalse(validator1.check_if_date_exists(self.incorrect_data['end_date'], 'end_date'))
        self.assertEqual('"end_date" is not exists or in the past',
                         validator1.errors['end_date'])
        self.assertTrue(validator2.check_if_date_exists(self.correct_data['end_date'], 'end_date'))

    def test_str_to_datetime(self, date='11/05/2020'):
        self.assertEqual(Validator.str_to_datetime(date), datetime.strptime(date, '%d/%m/%Y'))

    def test_validate_date_chronology(self):
        validator1 = Validator(self.incorrect_data_date_reverse)
        validator2 = Validator(self.correct_data)
        self.assertFalse(validator1.validate_date_chronology())
        self.assertEqual('"start_date" mast be earlier then "end_date"',
                         validator1.errors['start_date'])
        self.assertTrue(validator2.validate_date_chronology())

    def test_validate_lectures_number(self):
        validator = Validator(self.incorrect_data)
        validator.validate_lectures_number()
        self.assertEqual('Must be a digit',
                         validator.errors['lectures_number'])

    def test_validate_title_length(self):
        validator = Validator({
            'title': "1" * 129
        })
        validator.validate_title_length()
        self.assertEqual('Must be less then 128',
                         validator.errors['wrong_title_length'])

    def test_check_errors(self):
        validator1 = Validator(self.incorrect_data)
        validator2 = Validator(self.correct_data)
        validator2.check_errors()
        self.assertFalse(validator2.errors)
        validator1.check_errors()
        self.assertDictEqual(
            {'title': '"title" is required field',
             'start_date': 'Input "start_date" as dd/mm/yyyy',
             'lectures_number': 'Must be a digit'},
            validator1.errors
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
