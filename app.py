from courses import app, db
from courses import models, set_logger


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Course': models.Course,
    }


if __name__ == '__main__':
    app.run(debug=True)
