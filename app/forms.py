import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.database import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"oninput": "checkForm()"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"oninput": "checkForm()"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти', render_kw={"disabled": True})



class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"oninput": "checkForm()"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"oninput": "checkForm()"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"oninput": "checkForm()"})
    submit = SubmitField('Зарегистрироваться', render_kw={"disabled": True})

    def validate_username(self, username):
        pattern = '^[a-zA-Zа-яА-Я0-9_-]+$'
        if not re.match(pattern, username.data):
            raise ValidationError('Имя пользователя не может содержать\nпользовательские символы')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Эта почта уже использована.')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')