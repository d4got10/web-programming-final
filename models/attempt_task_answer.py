from app import db


class AttemptTaskAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Integer, db.ForeignKey('answer.id'))
    attempt_task = db.Column(db.Integer, db.ForeignKey('attempt_task.id'))
