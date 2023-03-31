from app import db


class AttemptTaskAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(512))
    attempt_task = db.Column(db.Integer, db.ForeignKey('attempt_task.id'))
