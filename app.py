from flask import Flask, render_template, redirect, url_for, request, flash
from flask_restful import Api
from extensions import db, ma, login_manager  # Importuj login_manager
from resources import TaskListResource, TaskResource, UserListResource
from config import Config
from models import Task, User
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user # Import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app) # Inicjalizacja LoginManagera

    api = Api(app)
    api.add_resource(TaskListResource, '/api/tasks')
    api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
    api.add_resource(UserListResource, '/api/users')

    @login_manager.user_loader  # Dekorator Flask-Login
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    @login_required  # Wymagaj zalogowania
    def index():
        users = User.query.all()
        return render_template('task_list.html', users=users, current_user=current_user) #Przekazanie current_user


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)  # Zaloguj użytkownika
                next_page = request.args.get('next') # Pobierz adres URL, do którego użytkownik próbował wejść
                return redirect(next_page or url_for('index')) # Przekieruj na stronę główną lub 'next'
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger') # Komunikat, kategoria bootstrap
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()  # Wyloguj użytkownika
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST']) #Rejestracja użytkownika
    def register():
        if current_user.is_authenticated: #Jeśli zalogowany przekieruj
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            color = request.form.get('color')

            #Walidacja
            if not username or not password or not color:
                flash('Please fill out all fields', 'danger')
                return render_template('register.html')

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return render_template('register.html')

            # Tworzenie i zapis usera
            new_user = User(username=username, color=color)
            new_user.set_password(password) # Haszowanie hasła
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login')) #Przekierowanie do logowania

        return render_template('register.html') #Wyświetlenie formularza

    return app

app = create_app()
