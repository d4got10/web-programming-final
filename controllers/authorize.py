from app import app
from flask import render_template

@app.route('/authorize/')
def authorize():  # put application's code here
    return "Authorization"#render_template('catalog.html')