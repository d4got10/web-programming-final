from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    description = db.Column(db.String(4096))
    attempts = db.relationship('Attempt', backref='attempt_course', lazy=True)
    tasks = db.relationship('Task', backref='task_course', lazy=True)


def get_popular_courses(count):
    #return [generate_test_course(i) for i in range(1, count + 1)]
    return Course.query.limit(count).all()


def get_course(id):
    return Course.query.filter_by(id=id).first()


def generate_test_course(index):
    return {
        'id': index,
        'name': f'Курс номер {index}',
        'description': f'Это описание шикарного курс под номером {index}. Проходите не пожалеете!',
    }

def populate_test_courses():
    for i in range(1, 10):
        course = Course(name=f'Курс номер {i}',
                        description=f'Это описание шикарного курса под номером {i}. Проходите не пожалеете!')
        db.session.add(course)
    db.session.commit()