from flask import request
from flask_restful import Resource, reqparse
from models import Task, User
from schemas import TaskSchema, UserSchema
from extensions import db
from datetime import datetime

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class TaskListResource(Resource):
    def get(self):
        # Na razie pobieramy wszystkie zadania (bez archiwizacji)
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)  # Przyjmujemy jako string ISO 8601
        parser.add_argument('priority', type=int)
        parser.add_argument('assigned_to_id', type=int, required=True, help='Assigned user is required')
        args = parser.parse_args()

        # Konwersja due_date (string -> datetime)
        if args['due_date']:
            try:
                args['due_date'] = datetime.fromisoformat(args['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return {'message': 'Invalid due_date format. Use ISO 8601.'}, 400

        new_task = Task(**args)
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task), 201


class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task_schema.dump(task)

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)
        parser.add_argument('priority', type=int)
        parser.add_argument('assigned_to_id', type=int)
        # completed, archived, in_progress - dodamy później
        args = parser.parse_args()

        # Konwersja due_date
        if args['due_date']:
            try:
                args['due_date'] = datetime.fromisoformat(args['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return {'message': 'Invalid due_date format. Use ISO 8601.'}, 400

        for key, value in args.items():
            if value is not None:
                setattr(task, key, value)

        db.session.commit()
        return task_schema.dump(task)

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
