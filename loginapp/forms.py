from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, \
                        SubmitField, validators

                        
# the flask wtf login form setup and validation
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")


class RegistForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()
        ])
    email = StringField("Email", validators=[
        validators.DataRequired(), 
        validators.Email()
        ])
    password = PasswordField("Password", validators=[validators.DataRequired(), 
        validators.EqualTo("vpassword", message="Passwords don't match")
        ])
    vpassword = PasswordField("Verify Password", validators=[
        validators.DataRequired()
        ])
    submit = SubmitField("Register")