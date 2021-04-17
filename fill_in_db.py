from courses import db
from courses.models import Course

course1 = Course(title='Python', start_date='01/01/2020', end_date='01/05/2020', lectures_number=20)
course2 = Course(title='Java', start_date='01/03/2020', end_date='01/07/2020', lectures_number=21)
course3 = Course(title='JS', start_date='01/06/2020', end_date='01/12/2020', lectures_number=15)
db.session.add(course1)
db.session.add(course2)
db.session.add(course3)
db.session.commit()
