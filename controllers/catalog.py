from app import app
from flask import render_template
from models.courses import get_courses_info

@app.route('/')
def catalog():  # put application's code here
    course_info_list = get_courses_info()
    return render_template('catalog.html', course_info_list=course_info_list, len=len, str=str)