# models.py is used for creating classes that we'll use repeatedly to populate our databases

# these are presets for creating our databases so we don't have to write SQL tables and queries, we'll automate that stuff instead

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets
# SQLAlchemy and Migrate: will take care of writing SQL queries into Python, which allows us to focus more on what data we want to pass to our database rather than how to pass it

# UUID stands for universally unique identifiers: great for creating independent items that won't clash with other items - in the same way that our SQL keys needed primary keys to stay unique, we need things like users to have unique ID numbers so that we don't accidentally delete users or have multiple users log in to the same account

# datetime imports the day and time it is called on

# Werkzeug is German for 'tool' and is a security package; the password hash tools we import allow us to make the password data that we store in our database secret, so that if we log in to look at our database, we can't see what users saved as their password

# Set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()
# this means that when we see db, we're actually just using aspects of SQLAlchemy, so that we don't instantiate SQLAlchemy a bazillion times
# Marshmallow is similar and also helps out with Migrations for moving data around
# LoginManager is a class that helps with logging users in and keeping them logged in. When our browser 'talks' to the LoginManager class, it simply requests the user id from our User class - useful for checking if users are already logged in or not

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
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

# The variables inside of our User class have a number of traits that sound very suspiciously similar to SQL data items.
# These are all aspects of our SQL that SQLAlchemy translates for us.
# The variables are all the headers of columns.
# Each time our User class gets instantiated, it adds the given data to the column mentioned. 
# We have columns for: id, first name, last name, email, password, authentication, token, and date.

# NEXT we have an init
# Since this is a class, we have to have one.
# We save all the parameters passed in to the class and give them the magic self word.
# Many of these also default to empty data points, i.e. password=''
# We set the token, calling on the 'secrets' import to generate a token.
# We pass in the 24 character length as an integer during the __init__ method
# The set_id method creates a unique id number that we'll use as a primary key, since it's unique. You don't want to use the name as primary key, in case multiple users have the same name.
# set_password generates a hash that makes it impossible for the database owner to see the actual password
# __repr__ method prints out at the end - this will show up in our terminal eventually

#NEXT Create the Contact class (data item that we're going to save in our database, which we'll allow users to look at later):
class Contact(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,email,phone_number,address,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.user_token = user_token


    def __repr__(self):
        return f'The following contact has been added to the phonebook: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

# NEXT call on Marshmallow finally- this basically is another function that is part of the process of uploading our data to our database. NOTE THAT THE FIELDS MUST MATCH OUR CONTACT CLASS HERE. If they don't, there will be errors:
class ContactSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','email','phone_number', 'address']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)