from app import db


class AttemptTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))
    attempt = db.Column(db.Integer, db.ForeignKey('attempt.id'))
    answers = db.relationship('AttemptTaskAnswer', backref='answer_attempt_task', lazy=True)
