from werkzeug.security import generate_password_hash
from flask import Flask, render_template, flash
from flask_login import current_user, login_user
import sqlalchemy as sa
from typing import Optional
from wtforms.validators import email

from app import db
from app.database import User
from werkzeug.utils import redirect
from app.forms import RegisterForm
from app import app

@app.route('/registration', methods=['GET'])
def registration(error_message: Optional[str] = None):
    if current_user.is_authenticated:
        return redirect('/account')
    form = RegisterForm()
    return render_template('registration.html', form=form, error_message=error_message)

@app.route('/registration', methods=['POST'])
def registration_process():
    if current_user.is_authenticated:
        return redirect('/account')
    form = RegisterForm()
    if form.validate_on_submit():
        username_: str = form.username.data
        email_: str = str(form.email.data)
        pass_hash_ = str(generate_password_hash(form.password.data))
        u = User(username = username_,
                 email = email_,
                 password_hash = pass_hash_)
        db.session.add(u)
        db.session.commit()
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if user.check_password(form.password.data):
            login_user(u, remember=True)
            return redirect('/account')
        else:
            return registration('Произошла ошибка. Попробуйте позже')
    else:
        return render_template('registration.html',
                               form=form,
                               error_message='Некоторые данные введены неверно')

