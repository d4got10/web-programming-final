from app import db
from models.task import Task


class AttemptTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))
    attempt = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    answers = db.relationship('AttemptTaskAnswer', backref='answer_attempt_task', lazy=True)


def get_tasks(attempt_task_list):
    ids = [x.id for x in attempt_task_list]
    a = db.session.query(Task).select_from(AttemptTask).join(Task) \
        .filter(AttemptTask.id.in_(ids)).all()
    return a


def get_completed_tasks(attempt_task_list):
    ids = [x.id for x in attempt_task_list]
    tasks = db.session.query(Task, AttemptTask).select_from(AttemptTask).join(Task) \
        .filter(AttemptTask.id.in_(ids)).all()

    result = []
    for (task, attempt_task) in tasks:
        system_answers = list(task.answers)
        user_answers = list(attempt_task.answers)
        correct_system_answers = [x.value for x in system_answers if x.is_correct]
        ok = len(correct_system_answers) == len(user_answers)
        for answer in user_answers:
            if answer.value not in correct_system_answers:
                ok = False
        if ok:
            result.append(task)
    return result


def get_failed_tasks(attempt_task_list):
    ids = [x.id for x in attempt_task_list]
    tasks = db.session.query(Task, AttemptTask).select_from(AttemptTask).join(Task) \
        .filter(AttemptTask.id.in_(ids)).all()

    result = []
    for (task, attempt_task) in tasks:
        system_answers = list(task.answers)
        user_answers = list(attempt_task.answers)
        if len(user_answers) > 0:
            correct_system_answers = [x.value for x in system_answers if x.is_correct]
            ok = len(correct_system_answers) == len(user_answers)
            for answer in user_answers:
                if answer.value not in correct_system_answers:
                    ok = False
            if not ok:
                result.append(task)
    return result
