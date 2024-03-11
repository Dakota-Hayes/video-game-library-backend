from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    admin = db.Column(db.String(75), default = "False")
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password='', g_auth_verify=False, admin="False"):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        self.admin = admin
        
    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_email(self, email):
        self.email = email

    def set_g_auth_verify(self, g_auth_verify):
        self.g_auth_verify = g_auth_verify
    
    def set_admin(admin):
        self.admin = admin

    def __repr__(self):
        return f'User {self.id, self.password, self.email, self.token, self.g_auth_verify, self.admin, self.date_created}'

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'password', 'email', 'token', 'g_auth_verify', 'admin', 'date_created']

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Game(db.Model):
    id = db.Column(db.String, primary_key=True)
    owner = db.Column(db.String(150), nullable = True, default='')
    title = db.Column(db.String(150), nullable = True, default='')
    version = db.Column(db.String(150), nullable = True, default = '')
    console = db.Column(db.String(150), nullable = True, default = '')
    publisher = db.Column(db.String(150), nullable = True, default = '')
    region = db.Column(db.String(75), nullable = True, default = '')
    completed = db.Column(db.String(75), nullable = True, default = "False")
    condition = db.Column(db.String(250), nullable = True, default = '')
    value = db.Column(db.String(75), nullable = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, owner = '', title = '', version ='', console ='', publisher='', region='', completed='False', condition='', value=0.00):
        self.id = self.set_id()
        self.owner = owner
        self.title = title
        self.version = version
        self.console = console
        self.publisher = publisher
        self.region = region
        self.completed = completed
        self.condition = condition
        self.value = value

    def set_id(self):
        return str(uuid.uuid4())

    def set_title(self, title):
        self.title = title

    def set_version(self, version):
        self.version = version
    
    def set_console(self, console):
        self.console = console

    def set_publisher(self, publisher):
        self.publisher = publisher

    def set_region(self, region):
        self.region = region

    def set_completed(self, completed):
        self.completed = completed

    def set_status(self, condition):
        self.condition = condition

    def set_value(self, value):
        self.value = value

    def set_date_created(self, date_created):
        self.date_created = date_created

    def __repr__(self):
        return f'Game {self.id,self.owner,self.title,self.version,self.console,self.publisher,self.region,self.completed,self.condition,self.value,self.date_created} '

class GameSchema(ma.Schema):
    class Meta:
        fields = ['id', 'owner', 'title', 'version', 'console', 'publisher', 'region', 'completed', 'condition', 'value', 'date_created']

game_schema = GameSchema()
games_schema = GameSchema(many=True)