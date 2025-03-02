from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # Pamiętaj o hashowaniu!
    color = db.Column(db.String(7), default='#ffffff')  # Kolor kafelków
    tasks = db.relationship('Task', backref='assigned_to', lazy=True)
    # completed_tasks nie jest potrzebne na razie

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    # completed_at i completed_by - dodamy później
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # archived i in_progress - dodamy później
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'
