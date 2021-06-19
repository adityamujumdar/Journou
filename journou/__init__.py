from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from time import gmtime, strftime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = '327568b5c9c8d18eaec28eac01d6ffdd'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aditya:123456@localhost/journoutest"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'alert alert-danger container-fluid w-25 mt-3'
socketio = SocketIO(app)

from journou import routes