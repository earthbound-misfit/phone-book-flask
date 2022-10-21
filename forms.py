# ensures users are giving us the right data when they're logging in - valid email addres, for example
# the ability to take data from users and change it is a critical part of back-end servers and websites

# Because Flask is so lightweight, we will often need to import external packages to help our Flask apps maintain functionality

# FlaskForm - gives us a number of modules designed to enhance and secure our data-collecting process from our forms - i.e. ensure users are providing the right type of data and also handle that data on submission

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

# StringField - ensures that user inputs a string
# PasswordField - prevents users from showing their password on-screen
# SubmitField - a button class that automatically ties it's submit-time data with the other FlaskForm fields
# Other types of fields from wtforms: IntegerField, RadioField, etc. - all HTML form types have wtforms counterparts that can be used

# Instantiate these classes inside another class:
class UserLoginForm(FlaskForm):
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  submit_button = SubmitField()
# both DataRequired and Email validators basically run something like Regex on the forms to ensure that we are being given the right data type and that we aren't handing in empty forms...without having to write the Regex ourselves

