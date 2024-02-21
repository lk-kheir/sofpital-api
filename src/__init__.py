from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# CORS(app)
# assuming that the frontend is running on port 5173
# making our application to accept requests from the frontend
# Explicitly allow requests from 'https://sofpital.vercel.app'
cors = CORS(app, resources={r"/api/*": {"origins": "https://sofpital-hu26uscgr-louzanizineddine.vercel.app"}})

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# To specify to track modifications of objects and emit signals
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

class Base(DeclarativeBase):
  pass
# sql alchemy instance
db = SQLAlchemy(model_class=Base)

#It sets up the necessary configurations for SQLAlchemy to work with your Flask application.
#It establishes a connection to the database specified in your app's configuration.
#It configures a session (which is used to interact with the database).
db.init_app(app)
 

# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

# import models to let the migrate tool know
from src.models.user_model import User
from src.models.tutor_model import Tutor
from src.models.learner_model import Learner
from src.models.post_model import Post
from src.models.offer_model import Offer
from src.models.meeting_model import Meeting

with app.app_context():
    db.create_all()

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix = "/api")