from flask import request
from flask_restful import Resource, reqparse
from models import Task, User
from schemas import TaskSchema, UserSchema
from extensions import db
from datetime import datetime
from flask_login import login_required, current_user  # Importuj


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class TaskListResource(Resource):
    @login_required # Zabezpiecz
    def get(self):
        tasks = Task.query.all()
        return tasks_schema.dump(tasks)

    @login_required # Zabezpiecz
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)
        parser.add_argument('priority', type=int)
        parser.add_argument('assigned_to_id', type=int, required=True, help='Assigned user is required')
        args = parser.parse_args()

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
    @login_required # Zabezpiecz
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task_schema.dump(task)

    @login_required # Zabezpiecz
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)
        parser.add_argument('priority', type=int)
        parser.add_argument('assigned_to_id', type=int)
        args = parser.parse_args()

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

    @login_required # Zabezpiecz
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204

class UserListResource(Resource):
    @login_required #Zabezpiecz, opcjonalnie, ale warto
    def get(self):
        #Zabezpieczenie by admin mógł zobaczyć userów
        if not current_user.is_admin:
            return {'message': 'Unauthorized'}, 403
        users = User.query.all()
        return users_schema.dump(users)
