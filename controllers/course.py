from app import app
from flask import render_template
from models.course import get_course, get_users_courses
from flask_login import current_user


@app.route('/course/<id>')
def course(id=None):
    return render_template('course.html', course=get_course(id))

@app.route('/my_courses')
def my_courses(id=None):
    course_info_list = get_users_courses(current_user.id)
    print(course_info_list)
    return render_template('catalog.html', title_name="Ваши курсы", course_info_list=course_info_list, len=len, str=str)
