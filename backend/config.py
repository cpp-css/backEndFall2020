import os
import subprocess
from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv(verbose=True)
VERSION = "1.0.0" # SEMVER
GIT_COMMIT = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()

# assume we're in production unless told otherwise
DEBUG = (os.getenv('DEBUG', 'false') == 'true')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app = Flask("css-backend")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{pw}@{host}/{db}'.format(
    user=DB_USERNAME, pw=DB_PASSWORD, host=DB_HOST, db=DB_NAME)
app.config['SQLALCHEMY_ECHO'] = DEBUG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
#migrate = Migrate(app, db)
