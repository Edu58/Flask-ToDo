from flask import Blueprint, render_template, request, flash, jsonify, json
from flask_login import login_required, current_user
from .models import Todo
from app import db

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        todo = request.form.get('todo')

        if len(todo) < 2:
            flash('Todo should be atlest 2 characters', category='error')
        else:
            new_todo = Todo(task=todo, user_id=current_user.id)

            db.session.add(new_todo)
            db.session.commit()

            flash('Todo added successfuly', category='success')

    return render_template('index.html', user=current_user)


@views.route('/delete-note', methods=["POST"])
@login_required
def delete_note():
    todo = json.loads(request.data)
    todoid = todo['todoId']
    get_todo = Todo.query.get(todoid)
    if get_todo:
        if get_todo.user_id == current_user.id:
            db.session.delete(get_todo)
            db.session.commit()
        return jsonify({})


