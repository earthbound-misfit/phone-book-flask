# the api portion of our Flask app is the location and rules of the server
# until we do this, our database has no content for users to view
# so here we create the stuff that actually does stuff for our front-end users to interact with - pull and push data to and from a server somewhere
# eventually we'll use HTML, CSS, JS and React to create a front-end website that displays our data
# this portion though only handles BACK-END data

# api folder will not have any templates, only routes
# this is because we're not returning any HTML, just data
# the data will be in a format known as JSON, which is related to JavaScript
# later we will find ways to parse that data, but for now - JSON is basically like a Python dictionary, they look and operate very similarly

# we import jsonify - this will take our data and put it in JSON format so that we can peruse the data using JS and Python

# we also have a slightly different Blueprint instantiation - now we have 'url_prefix='/api' - this means that all API calls will have to have /api before we insert our slugs

from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')

