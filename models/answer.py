from app import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(512))
    is_correct = db.Column(db.Integer)
    task = db.Column(db.Integer, db.ForeignKey('task.id'))
