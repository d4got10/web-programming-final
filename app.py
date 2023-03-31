from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models.user import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from controllers.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

import controllers.catalog
import controllers.course
import controllers.attempt
import controllers.profile

from models.attempt import Attempt
from models.course import Course
from models.answer import Answer
from models.task import Task
from models.attempt_task import AttemptTask
from models.attempt_task_answer import AttemptTaskAnswer

from models.course import populate_test_courses
from models.task import populate_tasks
from models.answer import populate_answers

def populate_database():
    populate_test_courses()
    for course in db.session.execute(db.select(Course)).scalars():
        populate_tasks(course.id, 30)
    populate_answers()


with app.app_context():
    db.create_all()
    #populate_database()


