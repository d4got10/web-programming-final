from app import db


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))