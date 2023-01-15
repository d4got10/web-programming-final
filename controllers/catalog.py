from app import app
from flask import render_template

@app.route('/')
def catalog():  # put application's code here
    return render_template('catalog.html')