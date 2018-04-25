# -*- coding: utf-8 -*-
import sys
import argparse
from flask import Flask, render_template, request, \
                    redirect, Response, url_for, abort
from urllib.parse import urlparse, urljoin
from flask_login import LoginManager, UserMixin, current_user, \
                                login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# flask app setup
app = Flask(__name__)
app.secret_key = "update_me"

# flask-login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# setup flask sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# the user model (flask login)
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# the flask wtf login form setup and validation
class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_username(self, field):
        if field.data != 'user':
            raise ValidationError("Invalid username")

    def validate_password(self, field):
        if field.data != 'password':
            raise ValidationError("Invalid password")


# the user table structure 
class DBUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<DBUser %r>' % self.username


# setup and populate the database
def setup_db():
    db.create_all()
    user_dict = {
        "admin" : DBUser(username='admin', email='admin@example.com', password='abc123'),
        "guest" : DBUser(username='guest', email='guest@example.com', password='password')}
    for key, user in user_dict.items():
        print("%s added to the database."% user.username)
        db.session.add(user)
    db.session.commit()

# snippet to check if the url is safe
# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# home page (non protected)
@app.route("/")
def home():
    return render_template("home.html")


# an example protected url
@app.route("/secret")
@login_required
def secret():
    return render_template("secret.html")


# login here
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            username = request.form["username"]
            user = User(len(username))
            login_user(user)

            next = request.args.get("next")
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for("home"))
        return render_template("login.html", form=form)
    else:
        return "Already logged in."


# log the user out
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# handle failed login
@app.errorhandler(401)
def page_not_found(e):
    return "Login failed"


# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An example usage of flask login.")
    parser.add_argument('-s', '--setup', dest='dbsetup', action='store_true',
                    help='This creates and sets up the base database.')
    parser.add_argument('-r', '--run', dest='run',  action='store_true',
                    help='Start and run the server.')
    parser.add_argument('-d', '--debug', dest='debug',  action='store_true',
                    help='Start the app in debug mode.')
    parser.add_argument('-l', '--listen', dest='host', default='127.0.0.1',
                    help='Where should the server listen. \
                          Defaults to 127.0.0.1.')
    parser.add_argument('-p', '--port', dest='port', default=5000,
                    help='Which port should the server listen on. \
                          Defaults to 5000.')
    # if no args were supplied print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    # we have args...let's do things
    args = parser.parse_args()
    if args.dbsetup and args.run:
        print("Setup and run arguments can't be used at the same time.")
        sys.exit(1)
    if args.dbsetup:
        setup_db()
    if args.run:
        app.run(debug=args.debug, host=args.host, port=args.port)