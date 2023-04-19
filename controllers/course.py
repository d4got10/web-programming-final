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

@app.route('/course/<id>')
def course(id=None):
    return render_template('course.html', course=get_course(id))

@app.route('/my_courses')
def my_courses(id=None):
    course_info_list = get_users_courses(current_user.id)
    authors = User.query.limit(100).all()
    print(course_info_list)
    return render_template('catalog.html',current_user_id=current_user.id, authors=authors, in_my_courses_list=True, title_name="Ваши курсы", course_info_list=course_info_list, len=len, str=str)

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
def edit_tasks_of_course(id=None, selected_task_id=None):
    course = request.form.get('course')
    user = request.form.get('user')
    tasks = get_task_list(id, 100, False)
    selected_task_id = request.values.get('selected_task_id')
    if request.values.get('edit-task'):

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

    elif request.values.get('submit-delete-task'):
        task_do_delete = get_task(request.values.get('selected_task_id'))
        db.session.delete(task_do_delete)
        db.session.commit()
        selected_task = None
        return redirect(url_for('edit_tasks_of_course', id=id))
    elif request.values.get('new-task'):
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
        return redirect(url_for('edit_tasks_of_course', id=id))
    elif request.values.get('selected_task_id'):
        selected_task = get_task(int(selected_task_id))
    else:
        selected_task = None
    return render_template('edit_course_tasks.html',
                           course=get_course(id),
                           user=user,
                           task_list=tasks,
                           selected_task=selected_task)
