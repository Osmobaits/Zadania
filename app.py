from flask import Flask, render_template, redirect, url_for, request, flash
from flask_restful import Api
from extensions import db, ma, login_manager
from resources import TaskListResource, TaskResource, UserListResource
from config import Config
from models import Task, User
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user
import os  # Importuj moduł os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    api = Api(app)
    api.add_resource(TaskListResource, '/api/tasks')
    api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
    api.add_resource(UserListResource, '/api/users')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    @login_required
    def index():
        users = User.query.all()
        return render_template('task_list.html', users=users, current_user=current_user)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            color = request.form.get('color')

            if not username or not password or not color:
                flash('Please fill out all fields', 'danger')
                return render_template('register.html')

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return render_template('register.html')

            new_user = User(username=username, color=color)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')
    # --- Funkcja do tworzenia administratora ---
    def create_admin():
        with app.app_context():
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')  # Pobierz z zmiennej środowiskowej lub użyj domyślnej
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin')  # Pobierz z zmiennej środowiskowej lub użyj domyślnej
            admin_color = os.environ.get('ADMIN_COLOR', '#ff0000') #Pobierz z env lub domyślny

            existing_admin = User.query.filter_by(username=admin_username).first()
            if not existing_admin: # Sprawdź, czy administrator już istnieje
                admin = User(username=admin_username, color=admin_color, is_admin=True)
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"Created admin user: {admin_username}")
            else:
                 print(f"Admin user '{admin_username}' already exists.")

    create_admin() # Wywołaj funkcję tworzącą administratora

    return app

app = create_app()
