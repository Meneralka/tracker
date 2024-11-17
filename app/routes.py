from flask import Flask, render_template, request
from datetime import datetime
from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from typing import Optional, List
from app import db
from app.database import User, Tasks, Sections
from werkzeug.utils import redirect
from app.forms import LoginForm
from app import app
from flask_login import logout_user

@app.route("/")
@login_required
def home():
    today_date = datetime.now().strftime('%d.%m.%Y')
    section = request.args.get('section')
    if section:
        req = sa.select(Tasks).where(Tasks.user_id == current_user.id, Tasks.section_url == section)
    else:
        req = sa.select(Tasks).where(Tasks.user_id == current_user.id)
    sections = db.session.scalars(
        sa.select(Sections).where(Sections.user_id == current_user.id)
    ).all()
    task_list: Optional[List] = db.session.scalars(req).all()
    return render_template('habits.html',
                           today_date=today_date,
                           task_list=task_list,
                           sections=sections)

@app.route("/login", methods=["GET"])
def login(error_message: Optional[str] = None):
    if current_user.is_authenticated:
        return redirect('/account')
    form = LoginForm()
    return render_template('login.html', form=form, error_message=error_message)


@app.route("/login", methods=["POST"])
def login_process():
    if current_user.is_authenticated:
        return redirect('/account')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )


        if user is None or not user.check_password(form.password.data):
            return login(error_message='Неверные логин или пароль')

        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    else:
        return render_template('login.html',
                               form=form,
                               error_message='Данные введены неверно')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
