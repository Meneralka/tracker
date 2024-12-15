from typing import Any

from flask_login import login_required, current_user
import sqlalchemy as sa
from werkzeug.local import LocalProxy

from app.database import User, Tasks, Sections
from app import db
from app import app
from app import database
from flask import request, jsonify
from app.forms import CreateTaskForm, changeStatusForm, CreateSectionForm, deleteTaskForm
import random, string

def randomUrl(length):
   letters = string.ascii_letters
   return ''.join(random.choice(letters) for i in range(length))

@app.route('/task/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id: int):
    req = sa.select(Tasks).where(Tasks.user_id == current_user.id,
                                     Tasks.id == task_id)
    task = db.session.scalar(req)
    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404
    return jsonify({'name': task.name, 'desc': task.desc, 'section_url': task.section_url, 'status': task.progress}), 200


@app.route('/task_create', methods=['POST'])
@login_required
def task_create():
    form = CreateTaskForm()
    if form.validate_on_submit():
        name = form.name.data
        desc = form.description.data
        category = form.category.data
        task = Tasks(name=name, desc=desc, user_id=current_user.id, section_url=category)
        db.session.add(task)
        db.session.commit()

        return jsonify({'message': 'ok', 'data':{'name':name, 'desc': desc}})

    else:
        errors = '\n'.join([i for i in form.errors])

        return jsonify({'message': errors})

@app.route('/section_create', methods=['POST'])
@login_required
def section_create():
    form = CreateSectionForm()
    if form.validate_on_submit():
        category = form.category.data
        section = Sections(section=category,
                           section_url=randomUrl(8),
                           user_id=current_user.id)
        db.session.add(section)
        db.session.commit()
        return jsonify({'message': 'ok', 'data':{'section':category}})

    else:
        errors = '\n'.join([i for i in form.errors])
        return jsonify({'message': errors}), 500

@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    form = deleteTaskForm()
    if form.validate_on_submit():
        req = sa.select(Tasks).where(Tasks.user_id == current_user.id,
                                     Tasks.id == form.task_id.data)
        task = db.session.scalar(req)
        if not task:
            return jsonify({'error': 'Задача не найдена'}), 404

        db.session.query(Tasks).where(Tasks.id == form.task_id.data).delete()
        db.session.commit()
        return jsonify({'message': 'ok'}), 200

    errors = '\n'.join([i for i in form.errors])
    return jsonify({'message': errors}), 500

@app.route('/change_status_task', methods=['POST'])
@login_required
def change_task_status():
    form = changeStatusForm()
    if form.validate_on_submit():
        req = db.session.scalar(
            sa.select(Tasks).where(Tasks.id == form.task_id.data, Tasks.user_id == current_user.id)
        )
        status = True if not req.progress else False
        db.session.query(Tasks).where(Tasks.id == form.task_id.data, Tasks.user_id == current_user.id
                                      ).update({'progress': status})
        db.session.commit()
        return jsonify({'message': req.progress})

    errors = '\n'.join([i for i in form.errors])
    return jsonify({'message': errors})