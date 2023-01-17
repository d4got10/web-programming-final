from app import app
from flask import render_template
from flask_login import current_user, login_required
from models.attempt import get_user_attempts


@app.route('/profile')
@login_required
def profile():
    attempts = get_user_attempts(current_user.id)
    return render_template('profile.html', attempts=attempts)
