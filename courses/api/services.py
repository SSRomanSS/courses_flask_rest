from sqlalchemy import and_


from courses.api.utils.validators import Validator


def find_courses(obj, data: dict) -> tuple:
    """
    Search courses with params
    :param obj: Course
    :param data: search parameters
    :return: (list of courses as dicts, flag)
    """
    if not data:
        return get_all_courses(obj)
    title = data.get('title')
    if title:
        return search_course_by_title(obj, title)
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if start_date and end_date:
        validator = Validator(data)
        return search_in_date_range(obj, validator, start_date, end_date)
    date = data.get('date')
    if date:
        validator = Validator(data)
        return search_current_courses(obj, validator, date)


def search_course_by_title(obj, title: str) -> tuple:
    """
    Get courses filtered by title
    :param obj: Course
    :param title: Course.title
    :return: (list of courses as dicts, flag)
    """
    courses = obj.query.filter_by(title=title).all()
    return create_courses_list(courses), 'success'


def search_in_date_range(obj, validator: Validator, start_date: str, end_date: str) -> tuple:
    """
    Search courses between to dates
    :param obj: Course
    :param validator: obj of class Validator
    :param start_date: start date
    :param end_date: end date
    :return: (list of courses as dicts, flag)
    """
    if validator.validate_date_chronology():
        start_date = validator.str_to_datetime(start_date)
        end_date = validator.str_to_datetime(end_date)
        courses = obj.query.filter(and_((obj.start_date >= start_date),
                                        (obj.end_date <= end_date))).all()
        return create_courses_list(courses), 'success'
    else:
        return validator.errors, 'error'


def search_current_courses(obj, validator: Validator, date: str) -> tuple:
    """
    Search all course which take place on a specified data
    :param obj: Course
    :param validator: obj of class Validator
    :param date: date for
    :return: (list of courses as dicts, flag) or (list of errors as dicts, flag)
    """
    if validator.check_if_date_exists(date, 'date'):
        datetime_obj = validator.str_to_datetime(date)
        courses = obj.query.filter(and_((obj.start_date <= datetime_obj),
                                        (obj.end_date >= datetime_obj))).all()
        return create_courses_list(courses), 'success'
    else:
        return validator.errors, 'error'


def get_all_courses(obj) -> tuple:
    """
    Get all courses
    :param obj: Course
    :return: (list of courses as dicts, flag)
    """
    return create_courses_list(obj.query.all()), 'success'


def create_courses_list(data: list) -> list:
    """
    Create list of courses as dicts from course objects list
    :param data: courses list
    :return: list courses as dicts or empty list
    """
    if data:
        return [course.to_dict() for course in data]
    else:
        return []
