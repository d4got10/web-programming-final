from app import app
from flask import render_template, request, redirect, url_for
from models.tasks import get_task_list
from flask_login import login_required, current_user, login_manager


@app.route('/new_attempt/', methods=['POST'])
def new_attempt():
    attempt_id = 1
    return redirect(url_for('attempt', id=attempt_id))


@app.route('/attempt/<id>')
@login_required
def attempt(id=None):
    course_id = 1
    task_list = get_task_list(course_id, 10)
    return render_template('attempt.html', task_list=task_list)
