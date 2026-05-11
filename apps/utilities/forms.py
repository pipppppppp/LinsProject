from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class SigninForm(FlaskForm):
    username = StringField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Username'})
    password = PasswordField('', validators=[InputRequired()], render_kw={'autofocus':True, 'placeholder':'Password'})


