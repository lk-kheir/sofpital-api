from src import db
from src.models.user_model import User
from src.models.learner_model import Learner
from src.models.tutor_model import Tutor
from src.models.offer_model import Offer
import base64
import bcrypt
from src import app
from datetime import datetime
from functools import wraps
from flask import request, jsonify
import jwt

time = "%Y-%m-%dT%H:%M:%S"
classes = {"user": User, "learner": Learner, "tutor": Tutor}

def to_dict(self):
    """returns a dictionary containing all keys/values of the instance"""
    new_dict = self.__dict__.copy()
    if 'profile_picture_blob' in new_dict and new_dict['profile_picture_blob'] is not None:
        new_dict['profile_picture_blob'] = base64.b64encode(new_dict['profile_picture_blob']).decode('utf-8')
    if "birthdate" in new_dict and new_dict["birthdate"] is not None:
        new_dict["birthdate"] = new_dict["birthdate"].strftime(time)
    if "last_time_online" in new_dict and new_dict["last_time_online"] is not None:
        new_dict["last_time_online"] = new_dict["last_time_online"].strftime(time)
    if "_sa_instance_state" in new_dict:
        del new_dict["_sa_instance_state"]
    return new_dict

def all(cls=None):
    """query on the current database session"""
    new_list = []
    # for clss in classes:
     #     if cls is None or cls is classes[clss] or cls is clss:
    if cls is not None:
        objs = cls.query.all()
        for obj in objs:
            # key = obj.__class__.__name__ + '.' + str(obj.id)
            new_list.append(to_dict(obj))
    return (new_list)

def get_by_id(cls, id):
    """query on the current database session"""
    if cls is not None:
        obj = cls.query.get(id)
        if obj is not None:
            return to_dict(obj)
    return None

def add(obj):
    """add an object to the current database session"""
    db.session.add(obj)
    db.session.commit()
    return obj

def delete(obj):
    """delete an object from the current database session"""
    db.session.delete(obj)
    db.session.commit()
    return obj

def update(obj):
    """update an object in the current database session"""
    db.session.commit()
    return obj

def check_unique_email(email):
    """check if email is unique"""
    if User.query.filter_by(email=email).first() is not None:
        return False
    return True

def check_unique_username(username):
    """check if username is unique"""
    if User.query.filter_by(username=username).first() is not None:
        return False
    return True

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['sub']).first()
        except:
            return jsonify({
                'message': 'Token is not valid'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)
    return decorated

def pagination(query, page, per_page):
    """returns a dictionary containing the pagination details"""
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    if query is not None:
        paginated_items = query[start_index:end_index]
    return paginated_items
# def is_strong_password(password):
#     # Check length
#     if len(password) < 8:
#         return False

#     # Check for at least one uppercase letter
#     if not re.search(r'[A-Z]', password):
#         return False

#     # Check for at least one lowercase letter
#     if not re.search(r'[a-z]', password):
#         return False

#     # Check for at least one digit
#     if not re.search(r'\d', password):
#         return False

#     # Check for at least one special character (excluding space)
#     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#         return False

#     # Check for no spaces
#     if ' ' in password:
#         return False

#     return True

# def is_valid_email(email):
#     # Define a regular expression for a basic email validation
#     email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

#     # Use re.match to check if the email matches the pattern
#     if re.match(email_regex, email):
#         return True
#     else:
#         return False

# def is_valid_phone_number(phone_number):
#     # Define a regular expression pattern for a basic phone number
#     pattern = re.compile(r'^\+?[0-9]{1,4}[\s.-]?[0-9]{1,15}$')

#     # Check if the phone number matches the pattern
#     return bool(re.match(pattern, phone_number))

# def is_valid_birthdate(birthdate_str):
#     try:
#         # Try to parse the date string
#         datetime.strptime(birthdate_str, '%Y-%m-%d')
#         return True
#     except ValueError:
#         # If parsing fails, it's an invalid date format
#         return False
    
# def validate_role(role):
#     if role not in ["tutor", "learner"]:
#         return False
#     return True

# def validate_gender(gender):
#     if gender not in ["male", "female"]:
#         return False
#     return True