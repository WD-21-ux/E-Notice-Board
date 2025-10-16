from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# SQLite DB file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///notices.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# import models here to ensure they are registered
from models import Notice

# Simple admin auth
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash("Admin login required", "warning")
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('index.html', notices=notices)

@app.route('/notice/<int:notice_id>')
def view_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    return render_template('view.html', notice=notice)

@app.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip() or 'Admin'
        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for('create'))
        notice = Notice(title=title, content=content, author=author)
        db.session.add(notice)
        db.session.commit()
        flash("Notice created.", "success")
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:notice_id>', methods=['GET', 'POST'])
@admin_required
def edit(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    if request.method == 'POST':
        notice.title = request.form.get('title', notice.title).strip()
        notice.content = request.form.get('content', notice.content).strip()
        notice.author = request.form.get('author', notice.author).strip() or notice.author
        db.session.commit()
        flash("Notice updated.", "success")
        return redirect(url_for('view_notice', notice_id=notice.id))
    return render_template('edit.html', notice=notice)

@app.route('/delete/<int:notice_id>', methods=['POST'])
@admin_required
def delete(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted.", "success")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or url_for('index')
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            flash("Logged in as admin.", "success")
            return redirect(next_url)
        else:
            flash("Incorrect password.", "danger")
            return redirect(url_for('login', next=next_url))
    return render_template('login.html', next=next_url)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
