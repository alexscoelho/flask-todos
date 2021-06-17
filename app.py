from flask import Flask, redirect, url_for, render_template, request, jsonify
import os
from models import db, User, Todo
from flask_migrate import Migrate
from datetime import datetime
# JWT
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_TOKEN_LOCATION"] = [
    "headers", "cookies", "json", "query_string"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

db.create_all()
migrate = Migrate(app, db)


@app.route("/login", methods=['POST', 'GET'])
def login():
    '''
    Login
    '''
    body = request.form
    if request.method == 'POST':
        email = body['email']
        password = body['password']
        query_user = User.query.filter_by(email=email).first()
        if password != query_user.password or email != query_user.email:
            return "Bad username or password"
        else:
            access_token = create_access_token(identity=email)
            response = redirect(url_for('index'))
            set_access_cookies(response, access_token)
            return response

    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    '''
    Signup
    '''
    body = request.form
    if request.method == 'POST':
        try:
            user = User(first_name=body['first_name'], last_name=body['last_name'],
                        email=body['email'], password=body['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return 'You Need to provide All Requested Information for creating an Account!!'

    return render_template('signup.html')


@app.route("/logout")
def logout():
    response = redirect(url_for('login'))
    unset_jwt_cookies(response)
    return response


@app.route("/")
@jwt_required()
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
    due_date = datetime.fromisoformat(body['due_date'])
    todo = Todo.query.filter_by(id=id).first()
    todo.name = body['name']
    todo.due_date = due_date
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/todo", methods=['POST'])
def add_todo():
    body = request.form
    try:
        due_date = datetime.fromisoformat(body['due_date'])
        todo = Todo(name=body['name'], due_date=due_date)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Please Specify Todo Name and Due Date"


@app.route('/done/<id>')
def done(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo is None:
        return "Todo not found"
    todo.completed = not(todo.completed)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/delete/<id>")
def delete_task(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo is None:
        return "Todo not found"
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000)
