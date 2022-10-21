# Import 'Blueprint'
# We are making the idea of these things - when we run the app is when we actually instantiate these objects, but here they are just functions and templates
# The Blueprint import allows us to use the templates and access the file structure around them

from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_templates')

# Because we want to keep our interests separate, we call this one 'site' instead of 'app' and we are going to end up importing a lot of this into our app

# The 'site' bit is telling our site to look inside of the site folder, and then the folder where the templates are located is called 'site_templates'

# So now we can import the variable 'site' into other Python files, like our __init__.py file and use all the data 

# To create our routes:

@site.route('/')
def home():
  return render_template('index.html')

@site.route('/profile')
def profile():
  return render_template('profile.html')