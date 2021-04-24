from flask import jsonify, request

from courses import db, app
from courses.api import api_bp
from courses.api.services import find_courses
from courses.api.utils.validators import Validator
from courses.models import Course


@api_bp.route('/courses', methods=['GET'])
def get_courses_list():
    # TODO add pagination
    params = request.args
    find_data = find_courses(Course, params)
    if not find_data[0]:
        return jsonify(message='Courses are not founded'), 404
    elif find_data[1] == 'error':
        return jsonify(message=find_data[0]), 400
    else:
        return jsonify(find_data[0])


@api_bp.route('/courses', methods=['POST'])
def create_post():
    data = request.get_json()
    validator = Validator(data)
    errors = validator.check_errors()
    if errors:
        return jsonify(message=errors), 400

    course = Course(
        title=data['title'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        lectures_number=data['lectures_number']
    )
    try:
        db.session.add(course)
        db.session.commit()
        return jsonify(message=f'{course} saved successfully'), 201
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return jsonify(message='Something went wrong'), 502


@api_bp.route('/courses/<int:id>', methods=['PUT'])
def update_post(id):
    data_from_request = request.get_json()
    course = Course.query.filter_by(id=id).first()
    if not course:
        return jsonify(message=f'Course {id} is not founded'), 404
    data_from_course = course.to_dict()
    data_from_course.update(data_from_request)
    validator = Validator(data_from_course)
    errors = validator.check_errors()
    if errors:
        return jsonify(message=errors), 400

    course.title = data_from_course['title']
    course.start_date = course.str_to_datetime(data_from_course['start_date'])
    course.end_date = course.str_to_datetime(data_from_course['end_date'])
    course.lectures_number = data_from_course['lectures_number']
    try:
        db.session.commit()
        return jsonify(message=f'{course} updated successfully'), 200
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return jsonify(message='Something went wrong'), 502


@api_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.filter_by(id=id).first()
    if not course:
        return jsonify(message=f'Course {id} is not founded'), 404
    return jsonify(course.to_dict())


@api_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    if not course:
        return jsonify(message=f'Course {id} is not founded'), 404
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify(message=f'{course} deleted successfully')
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        return jsonify(message='Something went wrong'), 400
