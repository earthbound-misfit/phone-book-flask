# helps make sure users can log in correctly and that they are actually authorized to access our api data

# this file essentially creates an extra function to check tokens for rightful access to data

# AND creates an encoder for our JSON content

from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User

# check to see if 'x-access-token' is in our headers for our API calls
# this process will help us modify the token in such a way that we can use the token and authenticate it
# it allows us to either modify the token OR send back specific errors detailing what's gone wrong if we make a faulty API cal
# Note that the function returns itself - this is unusual, but part of the checking process
# the *args and **kwargs are allowing us to continue adding more and more data to the process as long as we run the function
def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

# this checks that the instance of json are decimals, and then changes them into strings that we can use later
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)