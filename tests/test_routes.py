import unittest
import json
from courses import app, db
from courses.models import Course


class TestRouters(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()

        db.create_all()
        course1 = Course(title='Python', start_date='01/01/2021', end_date='01/05/2021', lectures_number=10)
        course2 = Course(title='Python', start_date='01/07/2021', end_date='01/10/2021', lectures_number=10)
        course3 = Course(title='Java', start_date='01/08/2021', end_date='01/11/2021', lectures_number=10)
        course4 = Course(title='JS', start_date='01/01/2022', end_date='01/05/2022', lectures_number=10)
        db.session.add_all([course1, course2, course3, course4])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_course(self):
        response1 = self.app.get('api/courses/3')
        self.assertEqual(response1.status_code, 200)
        response2 = self.app.get('api/courses/5')
        self.assertEqual(response1.get_json()['title'], 'Java')

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.get_json()['message'], 'Course 5 is not founded')
        self.assertEqual(response1.get_json()['title'], 'Java')

        response3 = self.app.post('api/courses/3')
        self.assertEqual(response3.status_code, 405)

    def test_delete_course(self):
        course = Course(title='Kotlin', start_date='01/01/2022', end_date='01/05/2022', lectures_number=10)
        db.session.add(course)
        response1 = self.app.delete('api/courses/5')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.get_json()['message'], 'Course Kotlin deleted successfully')

        response2 = self.app.delete('api/courses/5')
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(response2.get_json()['message'], 'Course 5 is not founded')

    def test_get_courses_list(self):
        response1 = self.app.get('api/courses')
        self.assertEqual(len(response1.get_json()), 4)
        self.assertEqual(response1.status_code, 200)

        response2 = self.app.get('api/courses?title=Python')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(response2.get_json()), 2)

        response3 = self.app.get('api/courses?date=01/09/2021')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(response3.get_json()), 2)
        self.assertEqual(response3.get_json()[0]['title'], 'Python')
        self.assertEqual(response3.get_json()[1]['title'], 'Java')

        response4 = self.app.get('api/courses?title=Basic')
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.get_json()['message'], 'Courses are not founded')

        response5 = self.app.get('api/courses?start_date=30/12/2021&end_date=02/05/2022')
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(len(response5.get_json()), 1)
        self.assertEqual(response5.get_json()[0]['title'], 'JS')

        response4 = self.app.get('api/courses?date=01/01/2030')
        self.assertEqual(response4.status_code, 404)
        self.assertEqual(response4.get_json()['message'], 'Courses are not founded')

    def test_create_post(self):
        payload1 = json.dumps(
            {
                'title': 'Go',
                'start_date': '01/01/2022',
                'end_date': '01/05/2022',
                'lectures_number': '10',
            }
        )
        response1 = self.app.post('api/courses', headers={'Content-Type': 'application/json'}, data=payload1)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(len(Course.query.filter_by(title='Go').all()), 1)
        payload2 = json.dumps(
            {
                'start_date': '01.01.2022',
                'end_date': '45/05/2022',
                'lectures_number': 'two',
            }
        )
        response2 = self.app.post('api/courses', headers={'Content-Type': 'application/json'}, data=payload2)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.get_json()['message'], {'title': '"title" is required field',
                                                           'start_date': 'Input "start_date" as dd/mm/yyyy',
                                                           'lectures_number': 'Must be a digit'})

    def test_update_post(self):
        payload = json.dumps(
            {
                'title': 'Ruby',
                'start_date': '01/01/2022',
                'end_date': '01/05/2022',
                'lectures_number': '10',
            }
        )
        response1 = self.app.put('api/courses/4', headers={'Content-Type': 'application/json'}, data=payload)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(Course.query.get(4).title, 'Ruby')

        response3 = self.app.post('api/courses/3')
        self.assertEqual(response3.status_code, 405)

        response3 = self.app.put('api/courses/25')
        self.assertEqual(response3.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
