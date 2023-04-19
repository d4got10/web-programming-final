from flask import render_template, request, redirect, url_for
from flask_login import current_user

from app import app
from app import db
from models.attempt_task import get_tasks
from models.course import get_course, get_users_courses, Course, delete_course
from models.task import get_task
from models.task import get_task_list
from models.user import User
from service.course_task_service import edit_task, delete_task, create_new_task


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
        selected_task = edit_task(selected_task_id)
    elif request.values.get('submit-delete-task'):
        delete_task()
        return redirect(url_for('edit_tasks_of_course', id=id))
    elif request.values.get('new-task'):
        create_new_task(id)
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





