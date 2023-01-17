from app import db
from models.task import Task


class AttemptTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))
    attempt = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    answers = db.relationship('AttemptTaskAnswer', backref='answer_attempt_task', lazy=True)


def get_tasks(attempt_task_list):
    ids = [x.id for x in attempt_task_list]
    a = db.session.query(Task).select_from(AttemptTask).join(Task)\
        .filter(AttemptTask.id.in_(ids)).all()
    return a