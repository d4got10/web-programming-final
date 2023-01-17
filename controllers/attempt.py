from app import app
from flask import render_template, request, redirect, url_for
from models.task import get_task_list
from flask_login import login_required, current_user, login_manager
from models.attempt import Attempt
from models.course import Course
from models.attempt_task import AttemptTask, get_tasks
from models.task import Task
from app import db
from datetime import datetime, timedelta

@app.route('/new_attempt/', methods=['POST'])
def new_attempt():
    course = request.form.get('course')
    user = request.form.get('user')
    model = Attempt(course=course, user=user, start_date=datetime.now(), end_date=datetime.now() + timedelta(hours=1))
    db.session.add(model)
    for task in get_task_list(course, 10):
        attempt_task = AttemptTask(
            attempt=model.id,
            task=task.id
        )
        db.session.add(attempt_task)
    db.session.commit()
    return redirect(url_for('attempt', id=model.id))


@app.route('/attempt/<id>')
@login_required
def attempt(id=None):
    selected_task = request.args.get('selected_task')
    if selected_task is None:
        selected_task = 1
    selected_task = int(selected_task) - 1
    print(selected_task)
    model = Attempt.query.filter_by(id=id).first()
    course = Course.query.filter_by(id=model.course).first()
    task_list = get_tasks(model.tasks) #list(get_task_list(course.id, 10))
    return render_template('attempt.html', attempt=model, task_list=task_list, course=course, selected_task=task_list[selected_task], len=len)
