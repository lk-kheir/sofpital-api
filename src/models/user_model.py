from src import db
from enum import Enum
from src import app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True, unique=True)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), nullable=False , unique=True)
    phone_number = db.Column(db.String(20), nullable=True , unique=True)
    birthdate = db.Column(db.Date(), nullable=True)
    password = db.Column(db.String(256), nullable=False)
    university = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(6), nullable=True)
    profile_picture_blob = db.Column(db.LargeBinary(), nullable=True)  # Store the image directly in the database
    online = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=False)
    last_time_online = db.Column(db.DateTime(), nullable=True)
    role = db.Column(db.String(10), nullable=False)
    tutor = db.relationship('Tutor', back_populates='user', uselist=False, cascade='all, delete-orphan, delete')
    learner = db.relationship('Learner', back_populates='user', uselist=False, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(self.password)
    
    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user
    

    def generate_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1000),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    
    def info(self):
        return f"User: {self.username} {self.email} {self.password}";