from app import app
from flask import render_template
from models.courses import get_popular_courses_info
from flask_login import current_user


@app.route('/')
def catalog():  # put application's code here
    course_info_list = get_popular_courses_info(9)
    return render_template('catalog.html', course_info_list=course_info_list, len=len, str=str)