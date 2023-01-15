from app import app
from flask import render_template

@app.route('/course/')
@app.route('/course/<id>')
def course(id=None):  # put application's code here
    return render_template('course.html', course=id)