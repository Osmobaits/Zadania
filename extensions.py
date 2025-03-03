from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager  # Importuj LoginManager

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()  # Dodaj LoginManager
login_manager.login_view = 'login'  # Ustaw widok logowania (adres URL)
login_manager.login_message_category = 'info' # kategoria (Bootstrap)
