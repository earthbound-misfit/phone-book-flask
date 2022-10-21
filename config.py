# Allows our application to talk to the internet
# Operates as a go-between for our app and either the servers we're hosting on (if we deploy it to the internet)
# or to talk to our computer and interface between our app

# This is all done before the app is even run
# We'll import os - this basically allows us to interface with the CLI and tell it commands

# first import os, which allows us to interface with the CLI and tell it commands
import os

# next: import functionality for loading a .env file, which is the other part of allowing our app to configure before it is run
from dotenv import load_dotenv

# then join the base directory (the line creating the basedir variable) and the .env file (the load_dotenv command takes care of this)
basedir = os.path.abspath(os.path.dirname(__file__)) 
load_dotenv(os.path.join(basedir, '.env'))

class Config():
  '''
    Set config variables for the flask app
    using Environment variables where available.
    Otherwise create the config variable if not done already.
  '''
  FLASK_APP = os.getenv('FLASK_APP')
  FLASK_ENV = os.getenv('FLASK_ENV')
  SECRET_KEY = os.environ.get('SECRET_KEY')

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_NOTIFICATIONS = False