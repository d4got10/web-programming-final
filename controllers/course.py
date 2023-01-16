from app import app
from flask import render_template
from models.courses import get_course_info
from flask_login import current_user


@app.route('/course/<id>')
def course(id=None):
    return render_template('course.html', course=get_course_info(id))
