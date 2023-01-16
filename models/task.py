from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    description = db.Column(db.String(4096))
    task_type = db.Column(db.Integer)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    answers = db.relationship('Answer', backref='answer_task', lazy=True)


def get_task_list(course_id, count):
    return [generate_task(course_id, i) for i in range(1, count + 1)]


def generate_task(course_id, index):
    return {
        'id': index,
        'name': f'Задание под номером {index}',
        'description': f'Описание задания под номером {index} для курса {course_id}',
        'task_type': 'single',
        'answers': ['Вариант ответа 1', 'Вариант ответа 2', 'Вариант ответа 3', 'Вариант ответа 4'],
        'correct_answer': [2]
    }