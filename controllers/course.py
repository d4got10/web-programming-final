from app import app
from flask import render_template, request
from models.course import get_course, get_users_courses, Course
from flask_login import current_user
from app import db

@app.route('/course/<id>')
def course(id=None):
    return render_template('course.html', course=get_course(id))

@app.route('/my_courses')
def my_courses(id=None):
    course_info_list = get_users_courses(current_user.id)
    print(course_info_list)
    return render_template('catalog.html', in_my_courses_list=True, title_name="Ваши курсы", course_info_list=course_info_list, len=len, str=str)

@app.route('/new_course', methods=['POST'])
def new_course(id=None):
    course_info_list = get_users_courses(current_user.id)
    course_name = request.form.get('course_name')
    course_description = request.form.get('course_description')
    course = Course(name=course_name, description=course_description, author_id=current_user.id)
    db.session.add(course)
    db.session.commit()
    return render_template('catalog.html', in_my_courses_list=True, title_name="Ваши курсы", course_info_list=course_info_list, len=len, str=str)
