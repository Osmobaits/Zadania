from extensions import db
from datetime import datetime
from flask_login import UserMixin  # Importuj UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # Importuj funkcje do hashowania

class User(db.Model, UserMixin):  # Dodaj UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Przechowuj hash hasła
    color = db.Column(db.String(7), default='#ffffff')
    tasks = db.relationship('Task', backref='assigned_to', lazy=True)
    is_admin = db.Column(db.Boolean, default=False) # Dodaj pole is_admin

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'
