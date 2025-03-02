from marshmallow import Schema, fields, validate
from extensions import ma
from models import User, Task

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)  # Kluczowe: Nie wysyłaj hasła!
        include_fk = True

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        include_fk = True

    assigned_to = ma.Nested(UserSchema, only=('id', 'username', 'color'))
    due_date = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%S", dump_only=True) #Tylko do odczytu
