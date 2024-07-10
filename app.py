from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"





@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print("post done")
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    # return jsonify({
    #     "sno": allTodo.sno,
    #     "title": allTodo.title,
    #     "desc": allTodo.desc
    # })
    return render_template("index.html", allTodo = allTodo)

@app.route('/products')
def products():
    allTodo = Todo.query.all()
    # print(allTodo)
    return "this is product page"

@app.route('/delete/<int:sno>', methods=['DELETE'])
def delete(sno):
    todo = Todo.query.get(sno)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    print("data deleted")
    return jsonify({"message": "Todo deleted successfully"})






@app.route('/update/<int:sno>', methods=['GET', 'PUT'])
def update(sno):
    if request.method == 'PUT':
        todo = Todo.query.get(sno)
        print(todo)
        data = request.get_json()   # Parse JSON data from the request
        print(data)
        if 'title' in data:
            todo.title = data['title']
        if 'desc' in data:
            todo.desc = data['desc']
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.get(sno)
    return render_template('update.html', todo = todo)

    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
