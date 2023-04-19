from app import db
from sqlalchemy.sql.expression import func

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    description = db.Column(db.String(4096))
    task_type = db.Column(db.Integer)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    answers = db.relationship('Answer', backref='answer_task', lazy=True)


def get_task_list(course_id, count, use_random):
    if (use_random):
        return list(db.session.execute(db.select(Task).filter_by(course=course_id).order_by(func.random()).limit(count)).scalars())
    else:
        return list(db.session.execute(
            db.select(Task).filter_by(course=course_id).limit(count)).scalars())

def get_task(task_id):
    return Task.query.filter_by(id=task_id).first()

def populate_tasks(course_id, count):
    for i in range(count):
        if i < count / 2:
            task = generate_task(course_id, i + 1, 1)
        elif i < count * 7 / 8:
            task = generate_task(course_id, i + 1, 2)
        else:
            task = generate_task(course_id, i + 1, 3)
        db.session.add(task)
    db.session.commit()


def generate_task(course_id, index, type):
    return Task(name=f'Задание c названием {index}',
                description=f'Описание задания c названием {index} для курса {course_id}',
                task_type=type,
                course=course_id)