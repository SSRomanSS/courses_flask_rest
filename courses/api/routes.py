from flask import jsonify, request

from courses import db
from courses.api import api_bp
from courses.api.utils.validators import Validator

from courses.models import Course



@api_bp.route('/courses', methods=['GET'])
def get_courses_list():
    return jsonify([course.to_dict() for course in Course.query.all()])


@api_bp.route('/courses', methods=['POST'])
def create_post():
    data = request.get_json()
    validator = Validator(data)
    errors = validator.check_errors()
    if errors:
        return jsonify(errors), 500
    else:
        course = Course(
            title=data['title'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            lectures_number=data['lectures_number']
        )
        try:
            db.session.add(course)
            db.session.commit()
            return jsonify(message=f'course {course} saved successfully'), 201
        except Exception:
            db.session.rollback()
            return jsonify(message='something went wrong'), 500


@api_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    return jsonify(Course.query.get_or_404(id).to_dict())


