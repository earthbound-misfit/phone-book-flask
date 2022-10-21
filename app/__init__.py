# This is what ultimately runs the entire app. Without it, nothing will happen.
# All the objects we've created - api, authentication, site, etc - come together in the init

# The init file is the FIRST THING THAT RUNS when we run our Flask app, so it's important to make sure that the init is basically the central hub of our app.
# This means we need to have clear logic when we're creating these - organization is key!

from flask import Flask
from config import Config
from .site.routes import site

# the period before site allows us to look around in our site folder - we locate the site folder that way and then we're looking inside of it for an object called 'site'

app = Flask(__name__)

# The above makes sure that Flask can run, but we haven't given it any data yet.
# To do this, we're going to use our structure to: 
# SEPARATE CONCERNS - this will mean that each folder and file will have a separate purpose
# By separating things, you make it much easier to solve individual problems with different aspects of our code.
# Part of the way we separate our concerns is with creating BLUEPRINTS in Flask
# Much like we made blueprint-like objects in OOP, or how a function is a blueprint of a process until we call the function.

# Now let's register the blueprint - this comes with Flask and should already be pulled in
# We'll tell it WHERE to register the blueprint to (app) and WHAT we're registering (the object which we imported)

app.register_blueprint(site)

# we will need some other data to talk to the browser before we can run the app, so we'll need to configure some settings for the browser and our command line interface to talk back and forth about what to expect from our app (this is done in config.py)

# Next we need to actually write the configuration:
app.config.from_object(Config)