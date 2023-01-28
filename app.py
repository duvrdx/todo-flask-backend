from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.app_context().push()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    state = db.Column(db.Boolean)

@app.route("/")
def index():
    try:
        ids = [item[0] for item in Todo.query.with_entities(Todo.id).all()]
        return ids
    except:
        return "400"

@app.route("/todo/add/<title>/<content>/<state>", methods=["POST", "GET"])
def add(title, content, state):
    try:
        if state == "true":
            state = True
        else:
            state = False

        db.session.add(Todo(title=title, content=content, state=state))
        db.session.commit()
        return "200"
    except:
        return "400"

@app.route("/todo/read/<id>", methods=["GET", "POST"])
def read(id):
    try:
        todo = Todo.query.get(int(id))
        if todo:
            return {"id": id, "title": todo.title, "content":todo.content, "state": todo.state}
        return "400"
    except:
        return "400"

@app.route("/todo/update/<id>/<title>/<content>/<state>", methods=["GET", "POST"])
def update(id, title, content, state):
    try:
        if state == "true":
            state = True
        else:
            state = False

        todo = Todo.query.get(int(id)) 
        todo.title = title
        todo.content = content
        todo.state = state

        db.session.commit()
        return "200"
    except:
        return "400"

@app.route("/todo/delete/<id>", methods=["GET", "POST"])
def delete(id):
    try:
        todo = Todo.query.get(int(id)) 
        db.session.delete(todo)
        db.session.commit()
        return "200"
    except:
        return "400"



if __name__ == "__main__":
    db.create_all()
    app.run()