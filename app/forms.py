import re

from flask_wtf import FlaskForm
from jinja2.utils import import_string
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, validators
from wtforms.fields.simple import TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email
import sqlalchemy as sa
from app import db
from app.icons import Icons
from app.database import User
from markupsafe import Markup


class LoginForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired()],
                           render_kw={"oninput": "checkForm()"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"oninput": "checkForm()"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти',
                         render_kw={"disabled": True})

class CreateTaskForm(FlaskForm):
    name = StringField('Название задачи',
                           validators=[validators.optional()],
                       render_kw={"oninput": "checkFormAddTask()",
                                  'placeholder':"Введите задачу"},

                       )
    category = SelectField('Выберите категорию:',
                           choices=[], coerce=str, validate_choice=False)

    description = TextAreaField('Описание задачи',
                              render_kw={'rows': 6, 'placeholder':"Введите описание задачи (необязательно)"}
                              )
    submit = SubmitField('Создать задачу',
                         render_kw={"disabled": ''}
                         )

class CreateSectionForm(FlaskForm):
    category = StringField('Название раздела',
                           validators=[DataRequired()],
                       render_kw={"oninput": "checkFormAddSection()",
                                  'placeholder':"Введите раздел"})
    submit = SubmitField('✔',
                         render_kw={"disabled": ''}
                         )

class RegisterForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired()],
                           render_kw={"oninput": "checkFormRegistration()"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"oninput": "checkFormRegistration()"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"oninput": "checkFormRegistration()"})
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

class deleteTaskForm():
    submit = SubmitField('&times;', render_kw={"disabled": True})

class changeStatusForm(FlaskForm):
    task_id = HiddenField(label="Task ID")
    submit = SubmitField()

class deleteTaskForm(FlaskForm):
    task_id = HiddenField("Task ID")
    submit = SubmitField('Удалить')

