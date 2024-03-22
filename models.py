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
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Portfolio(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    link = db.Column(db.String(255), nullable = False)
    repo_link = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,title,link,repo_link,date_created,user_token, id = ''):
        self.id = self.set_id()
        self.title = title
        self.link = link
        self.repo_link = repo_link
        self.date_created = date_created
        self.user_token = user_token


    def __repr__(self):
        return f'The following file has been added to the portfolio: {self.title}'

    def set_id(self):
        return (secrets.token_urlsafe())
    
class Resume(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, filename, file_path, uploaded_at, user_token, id=''):
        self.id = self.set_id()
        self.filename = filename
        self.file_path = file_path
        self.uploaded_at = uploaded_at
        self.user_token = user_token

    def __repr__(self):
        return f'The following file has been added to the portfolio: {self.filename}'

    def set_id(self):
        return secrets.token_urlsafe()

    

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title','link','repo_link','date_created']

class ResumeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'filename','file_path','uploaded_at']

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

resume_schema = ResumeSchema()
resumes_schema = ResumeSchema(many=True)

