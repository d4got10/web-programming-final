from app import app
from flask import render_template
from models.course import get_popular_courses
from flask_login import current_user


@app.route('/')
def catalog():  # put application's code here
    course_info_list = get_popular_courses(9)
    if (not current_user is None):
        return render_template('catalog.html', current_user_id=False, title_name="Все курсы",
                               course_info_list=course_info_list, len=len, str=str)
    return render_template('catalog.html', current_user_id=current_user.id, title_name="Все курсы", course_info_list=course_info_list, len=len, str=str)