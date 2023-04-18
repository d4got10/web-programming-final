from app import app
from flask import render_template, request, redirect, url_for
from models.course import get_course, get_users_courses, Course, get_last_id, delete_course
from models.attempt_task import AttemptTask, get_tasks, get_completed_tasks, get_failed_tasks
from models.attempt_task_answer import AttemptTaskAnswer
from models.task import Task, get_task_list, get_task
from models.attempt import Attempt
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, session
from models.task import get_task_list
from flask_login import current_user
from app import db

@app.route('/course/<id>')
def course(id=None):
    return render_template('course.html', course=get_course(id))

@app.route('/my_courses')
def my_courses(id=None):
    course_info_list = get_users_courses(current_user.id)
    print(course_info_list)
    return render_template('catalog.html',current_user_id=current_user.id,  in_my_courses_list=True, title_name="Ваши курсы", course_info_list=course_info_list, len=len, str=str)

@app.route('/new_course', methods=["POST", "GET"])
def new_course(id=None):
    if not request.form.get('submit'):
        return render_template('new_course.html',current_user_id=current_user.id,  in_my_courses_list=True, title_name="Ваши курсы", len=len, str=str)
    course_info_list = get_users_courses(current_user.id)
    course_name = request.form.get('course_name')
    course_description = request.form.get('course_description')
    course = Course(name=course_name, description=course_description, author_id=current_user.id)
    db.session.add(course)
    db.session.commit()
    print(course.id)
    return redirect(url_for('edit_course',id=str(course.id)))

@app.route('/edit_course/<id>')
def edit_course(id=None):
    if not request.values.get('course_name'):
        print('fff')
        return render_template('edit_course.html', course=get_course(id))
    if request.values.get('submit-delete'):
        delete_course(request.values.get('course'))
        return redirect(url_for('my_courses'))
    course = get_course(request.values.get('course'))
    course.name=request.values.get('course_name')
    course.description = request.values.get('course_description')
    print(course.id)
    print(course.name)
    print(course.description)
    task_list = get_tasks
    #db.session.add(course)
    db.session.commit()
    return render_template('edit_course.html', course=get_course(id))

@app.route('/edit_tasks_of_course/<id>', methods=["POST", "GET"])
def edit_answers_of_course(id=None, selected_task_id=None):
    course = request.form.get('course')
    user = request.form.get('user')
    tasks = get_task_list(id, 100, False)
    selected_task_id = request.values.get('selected_task_id')
    if request.values.get('submit-edit-task-description'):
        task_to_edit = get_task(request.values.get('selected_task_id'))
        task_to_edit.name = request.values.get('task_name')
        task_to_edit.description = request.values.get('task_description')
        db.session.commit()
    elif request.values.get('submit-delete-task'):
        task_do_delete = get_task(request.values.get('selected_task_id'))
        db.session.delete(task_do_delete)
        db.session.commit()
        selected_task = None
        return redirect(url_for('edit_answers_of_course', id=id))
    elif (request.values.get('selected_task_id')):
        selected_task = get_task(int(selected_task_id))
    else:
        selected_task = None
    return render_template('edit_course_tasks.html',  course=get_course(id), user=user, task_list=tasks, selected_task=selected_task)
