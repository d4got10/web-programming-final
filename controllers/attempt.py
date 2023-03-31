from app import app
from flask import render_template, request, redirect, url_for, session
from models.task import get_task_list
from flask_login import login_required, current_user, login_manager
from models.attempt import Attempt
from models.course import Course
from models.attempt_task import AttemptTask, get_tasks, get_completed_tasks, get_failed_tasks
from models.attempt_task_answer import AttemptTaskAnswer
from models.task import Task
from app import db
from datetime import datetime, timedelta

@app.route('/new_attempt/', methods=['POST'])
def new_attempt():
    course = request.form.get('course')
    user = request.form.get('user')
    model = Attempt(course=course, user=user, start_date=datetime.now(), end_date=datetime.now() + timedelta(minutes=1))
    db.session.add(model)
    for task in get_task_list(course, 10):
        attempt_task = AttemptTask(
            attempt=model.id,
            task=task.id
        )
        db.session.add(attempt_task)
    db.session.commit()
    session['new_attempt'] = model.id
    return redirect(url_for('attempt', id=model.id))

@app.route('/bind_attempt/<id>', methods=['GET'])
@login_required
def bind_attempt(id=None):
    model = Attempt.query.filter_by(id=id).first()
    model.user = current_user.id
    db.session.commit()
    return redirect(url_for('attempt', id=id))

@app.route('/attempt/<id>')
@login_required
def attempt(id=None):
    selected_task_id = request.args.get('selected_task')
    if selected_task_id is None:
        selected_task_id = 1
    selected_task_id = int(selected_task_id) - 1

    model = Attempt.query.filter_by(id=id).first()
    course = Course.query.filter_by(id=model.course).first()

    attempt_task_list = list(model.tasks)
    task_list = get_tasks(attempt_task_list)
    completed_task_list = get_completed_tasks(attempt_task_list)
    selected_task = task_list[selected_task_id]
    selected_attempt_task = attempt_task_list[selected_task_id]

    if datetime.now() < model.end_date:
        failed_task_list = get_failed_tasks(attempt_task_list)
    else:
        failed_task_list = [x for x in task_list if x not in completed_task_list]

    attempt_task = attempt_task_list[selected_task_id]
    user_answers = [x.value for x in attempt_task.answers]

    status = 'none'
    if selected_task in completed_task_list:
        status = 'completed'
    elif selected_task in failed_task_list:
        status = 'failed'

    return render_template(
        'attempt.html',
        attempt=model,
        task_list=task_list,
        course=course,
        selected_task_id=selected_task_id + 1,
        selected_attempt_task=selected_attempt_task,
        selected_task=selected_task,
        len=len,
        failed_task_list=failed_task_list,
        completed_task_list=completed_task_list,
        answers=task_list[selected_task_id].answers,
        selected_task_status=status,
        user_answers=user_answers,
        datetime=datetime
    )


@app.route('/attempt/<id>', methods=['POST'])
@login_required
def attempt_answer(id=None):
    model = Attempt.query.filter_by(id=id).first()
    selected_task = request.args.get('selected_task')

    if datetime.now() < model.end_date:
        answers = request.form.getlist('answers')
        answer = request.form.get('answer')
        if answer is not None:
            answers.append(answer)
        task_id = request.form.get('task')
        task = AttemptTask.query.filter_by(id=task_id).first()
        for answer in answers:
            task_answer = AttemptTaskAnswer(
                attempt_task=task.id,
                value=answer
            )
            db.session.add(task_answer)
        db.session.commit()

    return redirect(url_for('attempt', id=id, selected_task=selected_task))


@app.route('/attempt/close/<id>', methods=['POST'])
@login_required
def close_attempt(id=None):
    model = Attempt.query.filter_by(id=id).first()
    if datetime.now() < model.end_date:
        model.end_date = datetime.now()
        db.session.commit()
    selected_task = request.args.get('selected_task')
    return redirect(url_for('attempt', id=id, selected_task=selected_task))
