from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from badge import badges_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.register_blueprint(badges_bp)
migrate = Migrate()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SECRET_KEY'] = 'acdddb355a49957bf9f48604'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = ""

from recipe.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from recipe import routes
