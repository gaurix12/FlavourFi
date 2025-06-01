from recipe import db
from flask_login import UserMixin
from recipe import bcrypt


class User(db.Model, UserMixin):

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    badge = db.Column(db.String(80), default='Newbie')


class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    ingredients = db.Column(db.String(), nullable=False)
    instructions = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'
