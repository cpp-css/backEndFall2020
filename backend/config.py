import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv(verbose=True)

# assume we're in production unless told otherwise
DEBUG = (os.getenv('DEBUG', 'false') == 'true')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app = Flask("css-backend")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{host}/{db}'.format(
                                                                                    user=DB_USERNAME,
                                                                                    pw=DB_PASSWORD,
                                                                                    host=DB_HOST,
                                                                                    db=DB_NAME)
app.config['SQLALCHEMY_ECHO'] = DEBUG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)
