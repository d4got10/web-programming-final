from app import db
from models.task import Task
from random import randint


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(512))
    is_correct = db.Column(db.Integer)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))


def populate_answers():
    for task in db.session.execute(db.select(Task)).scalars():
        if task.task_type == 1:
            correct = randint(0, 3)
            for i in range(4):
                answer = Answer(value=f'Вариант ответа номер {i + 1}',
                                is_correct=(i == correct),
                                task=task.id)
                db.session.add(answer)
            pass
        elif task.task_type == 2:
            correct = {randint(0, 6), randint(0, 6), randint(0, 6)}
            for i in range(6):
                answer = Answer(value='Вариант ответа номер 1',
                                is_correct=(i in correct),
                                task=task.id)
                db.session.add(answer)
            pass
        else:
            answer = Answer(value="42",
                            is_correct=True,
                            task=task.id)
            db.session.add(answer)
            pass
    db.session.commit()
