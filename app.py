from flask import Flask
from flask_restful import Api
from extensions import db, ma
from resources import TaskListResource, TaskResource, UserListResource
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)

    api = Api(app)
    api.add_resource(TaskListResource, '/tasks')
    api.add_resource(TaskResource, '/tasks/<int:task_id>')
    api.add_resource(UserListResource, '/users') # Potrzebne do pobierania listy użytkowników

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
