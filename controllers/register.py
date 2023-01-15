from app import app
from flask import render_template

@app.route('/register/')
def register():  # put application's code here
    return "Registration"#render_template('catalog.html')