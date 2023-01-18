from datetime import datetime

from app import app
from flask import render_template
from flask_login import current_user, login_required
from models.attempt import get_user_attempts
from models.attempt_task import get_tasks, get_completed_tasks, get_failed_tasks


class Object(object):
    pass

@app.route('/profile')
@login_required
def profile():
    attempts = get_user_attempts(current_user.id)
    closed = []
    open = []
    for attempt in attempts:
        temp = Object()
        attempt_task_list = list(attempt[0].tasks)
        task_list = get_tasks(attempt_task_list)
        completed_task_list = get_completed_tasks(attempt_task_list)
        temp.attempt = attempt[0]
        temp.course = attempt[1]
        temp.completed_count = len(completed_task_list)
        temp.failed_count = len(get_failed_tasks(attempt_task_list))
        temp.task_count = len(task_list)
        if temp.attempt.end_date < datetime.now():
            closed.append(temp)
        else:
            open.append(temp)
    return render_template('profile.html', closed=closed, open=open)
