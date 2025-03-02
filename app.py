from flask import Flask, render_template, redirect, url_for
from flask_restful import Api
from extensions import db, ma
from resources import TaskListResource, TaskResource, UserListResource
from config import Config
from models import Task, User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    api = Api(app)
    api.add_resource(TaskListResource, '/api/tasks')
    api.add_resource(TaskResource, '/api/tasks/<int:task_id>')
    api.add_resource(UserListResource, '/api/users')

    @app.route('/')
    def index():
        users = User.query.all() #Pobierz dla kolorów
        return render_template('task_list.html', users=users)

    @app.route('/add_user', methods=['POST'])
    def add_user():
        from flask import request
        username = request.form.get('username')
        password = request.form.get('password')  # TODO: Hashowanie!
        color = request.form.get('color')

        if username and password and color:
            new_user = User(username=username, password=password, color=color)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('index'))


    with app.app_context():
        db.create_all()

    return app

# --- ZMIANY TUTAJ ---
app = create_app()  # Przypisz instancję aplikacji do zmiennej 'app'

if __name__ == '__main__':
    # NIE URUCHAMIAJ TEGO NA PRODUKCJI (OnRender)!
    # app.run(debug=True)
    pass #Zostaw puste, OnRender sam uruchomi
