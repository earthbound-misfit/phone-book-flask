from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# methods here are part of what gets sent from the browser
# Getting and Posting are different methods that a browser uses to categorize whether it is getting or giving away data
# in this case, we will be uploading data to our server, and checking data as well, so we need both methods - one to send, and one to pull back and check
@auth.route('/signup', methods = ['GET', 'POST'])

# instantiate a UserLoginForm, imported from forms.py
# we then use a try - except setup to handle any errors we get with the sign up process - if the database doesn't like what we give it, we will have an error
# the if statement asks if the browser is trying to post data, then continues if the form is submitted
# the data in the email variable - form.email.data - comes from the UserLoginForm class ('form' is the data from the class)
# Password does the same thing, and then we print them both out
# If a user creates an account, we should see that data show up in our CLI

# Next we add the user to the database with the db.session
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

# The 'user' variable is an instantiation of the User class from models.py 
# it includes the data passed in on forms.py as part of its creation
# NOTE if you're lost, follow the variables
# Use the magnifying glass search function in VS Code to find where things are originally declared            

            user = User(email, password = password)

# Now we add the user to the database with the db.session.add(user) and db.session.commit() lines - note their similarity to Git commands
            db.session.add(user)
            db.session.commit()


# Finally, we have a flashed message that executes when user account has been successfully created
            flash(f'You have successfully created a user account {email}', 'User-created')
# After code executes successfully, we return redirect, which will send us a different page than the one we're on. 
# So as soon as we successfully submit our data, this function will send us back to the home page:
            return redirect(url_for('site.home'))

# Now we write the except statement after we have the return redirect (should be tabbed to the same space as the try)
# the 'except' allows us to handle the problem if our users don't send good data to our database
# also what takes care of things if our FlaskForms and wtforms fields throw errors - in case things aren't validated:
    except:
        raise Exception('Invalid form data: Please check your form')
# finally, we render the template 'sign_up.html' as part of the original method
# and pass in form as form - this is so that our FlaskForms stuff gets injected into the HTML, because that is where all the actual data comes from
    return render_template('sign_up.html', form=form)

# Next

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

# logged_user variable will ask our User class to save the current user's name as a variable
# if nothing comes back from our data, then that user doesn't exist
# if the variable doesn't have any data stored to it, it will evaluate as falsy on the following line in the if statement, which will cause the else statement to run instead since our user isn't signed up for access to the content
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
# also have the login_user function that we brought in from the imports to actually log in our user, and hten it will redirect to our site.profile page
                login_user(logged_user)
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-success')
# url_for - this is us telling Flask to return the HTML for a certain file without having to call a method - we can just tell it to figure out what the URL is to locate the document
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

# this function logs users out with the logout_user function and sends them back to the home page
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))