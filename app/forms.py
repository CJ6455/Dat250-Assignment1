from wsgiref import validate
from xml.dom import ValidationErr
from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField, validators
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileAllowed

from config import Config
import re

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields
# TODO: Add validation, maybe use wtforms.validators??
# TODO: There was some important security feature that wtforms provides, but I don't remember what; implement it

  
class LoginForm(FlaskForm):
    username = StringField('Username',[validators.DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',[validators.DataRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remember me') # TODO: It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField('Sign In')
    recaptcha=RecaptchaField()
    

class RegisterForm(FlaskForm):
    first_name = StringField('First Name',[validators.DataRequired(),validators.Regexp('^[A-Za-z]+$',message='Only letters allowed!')], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name',[validators.DataRequired(),validators.Regexp('^[A-Za-z]+$',message='Only letters allowed!')], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username',[validators.DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',[validators.DataRequired(),validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$",message='password must contain, Uppercase, Lowercase, Numbers, and Special Characters and be between 6-20 characters')], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')
    

class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegisterForm)

class PostForm(FlaskForm):
    content = TextAreaField('New Post',[validators.DataRequired()], render_kw={'placeholder': 'What are you thinking about?'})
    image = FileField('Image',validators=[FileAllowed(Config.ALLOWED_EXTENSIONS,'Image only!')]) #sjekke om filtypen er tillatt
    submit = SubmitField('Post')

class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment',[validators.DataRequired()], render_kw={'placeholder': 'What do you have to say?'})
    submit = SubmitField('Comment')

class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username',[validators.DataRequired()], render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')

class ProfileForm(FlaskForm):
    education = StringField('Education', render_kw={'placeholder': 'Highest education'})
    employment = StringField('Employment', render_kw={'placeholder': 'Current employment'})
    music = StringField('Favorite song', render_kw={'placeholder': 'Favorite song'})
    movie = StringField('Favorite movie', render_kw={'placeholder': 'Favorite movie'})
    nationality = StringField('Nationality', render_kw={'placeholder': 'Your nationality'})
    birthday = DateField('Birthday')
    submit = SubmitField('Update Profile')
