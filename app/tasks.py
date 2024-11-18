from idlelib.iomenu import errors

from flask_login import login_required, current_user
from unicodedata import category

from app.database import User, Tasks
from app import db
from app import app
from app import database
from flask import request, jsonify

from app.forms import CreateTaskForm
from app.routes import home

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
        print(form.errors)
        errors = '\n'.join([i for i in form.errors])

        return jsonify({'message': errors})