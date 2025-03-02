from flask import Flask, render_template, redirect, url_for
from flask_restful import Api
from extensions import db, ma
from resources import TaskListResource, TaskResource, UserListResource  # Importuj zasoby
from config import Config
from models import Task, User  # Importuj modele


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    ma.init_app(app)

    # Inicjalizacja API
    api = Api(app)
    api.add_resource(TaskListResource, '/api/tasks')  # Dodajemy prefix /api
    api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
    api.add_resource(UserListResource, '/api/users')


    # Trasy dla widoków (renderowanie szablonów)
    @app.route('/')
    def index():
        #Pobierz wszystkich użytkowników, aby przekazać do szablonu
        # To jest potrzebne dla kolorów kafelków, nawet jeśli nie ma jeszcze API
        users = User.query.all()
        return render_template('task_list.html', users=users) #Przekazanie users

    @app.route('/add_user', methods=['POST']) #Tymczasowy endpoint do dodania usera
    def add_user():
        from flask import request # Importuj request wewnątrz funkcji
        username = request.form.get('username')
        password = request.form.get('password')  # TODO: Hashowanie!
        color = request.form.get('color')

        if username and password and color: #Prosta walidacja
            new_user = User(username=username, password=password, color=color)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('index'))

    # Utwórz tabele bazy danych (tylko raz, przy pierwszym uruchomieniu)
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # Uruchom w trybie debugowania (tylko do developmentu!)
