from flask_login import login_required
from app.database import User
from app import db
from app import app
from app import database
from flask import request, jsonify

@app.route('/task_create', methods=['POST'])
def task_create():
    data = request.json
    print(data)
    return jsonify({'data': 'okay'})
