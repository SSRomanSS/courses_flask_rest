from datetime import datetime

from flask import url_for

from courses import db


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    lectures_number = db.Column(db.Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('start_date') and kwargs.get('end_date') and kwargs.get('lectures_number'):
            self.start_date = self.str_to_datetime(kwargs['start_date'])
            self.end_date = self.str_to_datetime(kwargs['end_date'])
            self.lectures_number = int(kwargs['lectures_number'])

    def __repr__(self):
        return f'Course {self.title}'

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'start_date': self.datetime_to_str(self.start_date),
            'end_date': self.datetime_to_str(self.end_date),
            'lectures_number': self.lectures_number,
            "_links": {
                "self": url_for('api.get_course', id=self.id),
            }
        }

    @staticmethod
    def str_to_datetime(date_as_str: str) -> datetime:
        return datetime.strptime(date_as_str, '%d/%m/%Y')

    @staticmethod
    def datetime_to_str(date_as_datetime: datetime) -> str:
        return date_as_datetime.strftime('%d/%m/%Y')
