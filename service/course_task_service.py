from app import app
from flask import render_template, request, redirect, url_for
from models.course import get_course, get_users_courses, Course, get_last_id, delete_course
from models.attempt_task import AttemptTask, get_tasks, get_completed_tasks, get_failed_tasks
from models.attempt_task_answer import AttemptTaskAnswer
from models.task import Task, get_task_list, get_task
from models.user import User
from models.answer import Answer
from models.attempt import Attempt
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, session
from models.task import get_task_list
from flask_login import current_user
from app import db

def edit_task(selected_task_id):
    task_to_edit = get_task(request.values.get('selected_task_id'))
    task_to_edit.name = request.values.get('task_name')
    task_to_edit.description = request.values.get('task_description')
    selected_task = get_task(int(selected_task_id))
    if task_to_edit.task_type != 3:
        correct_answers = [int(v) for v in request.form.getlist('correct-answers[]')]
        for answer in task_to_edit.answers:
            answer.is_correct = 1 if answer.id in correct_answers else 0
    answers = request.form.getlist('ans[]')
    for i in range(len(task_to_edit.answers)):
        task_to_edit.answers[i].value = answers[i]
    db.session.commit()
    return selected_task

def create_new_task(id):
    task_type = request.form.get('task-type')
    task_type_by_name = {
        'single': 1,
        'multiple': 2,
        'text': 3
    }
    new_task = Task(course=id,
                    name=request.values.get('task_name'),
                    description=request.values.get('task_description'),
                    task_type=task_type_by_name[task_type])
    answers = request.form.getlist('ans[]')
    db.session.add(new_task)
    db.session.commit()
    db.session.refresh(new_task)
    if task_type == 'text':
        correct_answers = [1]
    else:
        correct_answers = [int(v) for v in request.form.getlist('correct-answers[]')]
    index = 1
    for answer in answers:
        is_correct = index in correct_answers
        task_answer = Answer(value=answer, is_correct=is_correct, task=new_task.id)
        db.session.add(task_answer)
        index += 1
    db.session.commit()


def delete_task():
    task_do_delete = get_task(request.values.get('selected_task_id'))
    db.session.delete(task_do_delete)
    db.session.commit()
    selected_task = None