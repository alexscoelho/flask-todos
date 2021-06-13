from flask import Flask, redirect, url_for, render_template, request
from models import db, User, Todo
from flask_migrate import Migrate

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

db.create_all()
migrate = Migrate(app, db)


@app.route("/")
def index():
    '''
    Home page
    '''
    todos = Todo.query.all()
    all_todos = list(map(lambda x: x.serialize(), todos))
    return render_template('index.html',  all_todos=all_todos)


@app.route("/sort")
def sort_todos():
    todos = Todo.query.order_by(Todo.name).all()
    all_todos = list(map(lambda x: x.serialize(), todos))
    return render_template('index.html',  all_todos=all_todos)


@app.route("/edit/<id>", methods=['PUT'])
def edit_todos(id):
    body = request.form
    print("/////////", body)
    todo = Todo.query.filter_by(id=id).first()
    todo.name = body['name']
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/todo", methods=['POST'])
def add_todo():
    body = request.form
    print("/////////", body)
    todo = Todo(name=body['name'])
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/done/<id>')
def done(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.completed = not(todo.completed)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/delete/<id>")
def delete_task(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000)
