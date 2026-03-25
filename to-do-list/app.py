from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Home
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, now=datetime.utcnow())

# Add task
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')

    new_task = Task(title=title, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

# Toggle complete
@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for('index'))

# Edit task
@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)

    task.title = request.form['title']
    task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%dT%H:%M')

    db.session.commit()
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
