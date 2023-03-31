from app import db
from models.course import Course


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    tasks = db.relationship('AttemptTask', backref='attempt_task', lazy=True)


def get_user_attempts(user_id):
    return db.session.query(Attempt, Course)\
        .join(Course)\
        .filter(Attempt.user == user_id)\
        .order_by(Attempt.start_date.desc())\
        .all()
