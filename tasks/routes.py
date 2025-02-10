from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import db, Task  
import os
from functools import wraps
from flask import current_app as app

tasks_bp = Blueprint('tasks', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', tasks=tasks)

@tasks_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    file = request.files['file']
    file_path = None
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    new_task = Task(title=title, user_id=session['user_id'], file_path=file_path)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks.dashboard'))
