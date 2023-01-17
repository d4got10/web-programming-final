from app import db


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    tasks = db.relationship('AttemptTask', backref='attempt_task', lazy=True)
