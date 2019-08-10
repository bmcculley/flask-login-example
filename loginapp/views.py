from flask import escape, render_template, request, flash, \
                    redirect, Response, url_for, abort
from flask_login import UserMixin, current_user, \
                            login_required, login_user, logout_user
from urllib.parse import urlparse, urljoin
from loginapp import app, db, login_manager, logger
from loginapp.forms import LoginForm, RegistForm
from loginapp import models
import bcrypt

# the user model (flask login)
class User(UserMixin):

    def __init__(self, id):
        user_data = models.DBUser.query.filter_by(id=id).first()
        self.id = id
        self.name = user_data.username
        self.email = user_data.email
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.email)


# snippet to check if the url is safe
# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
           ref_url.netloc == test_url.netloc
           

@app.route("/")
def home():
    return render_template("home.html")


# an example protected url
@app.route("/secret")
@login_required
def secret():
    return render_template("secret.html")


# register here
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if current_user.is_anonymous:
        form = RegistForm(request.form)
        if request.method == "POST" and form.validate():
            try:
                user = models.DBUser(username=form.username.data, 
                    email=form.email.data, 
                    password=bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt()))
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            except:
                # need to improve this error handling
                error = "Username or email already in use."
        return render_template("register.html", form=form, error=error)
    else:
        return redirect(url_for("home"))

# login here
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if current_user.is_anonymous:
        form = LoginForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            password = form.password.data.encode("utf-8")
            user_data = models.DBUser.query.filter_by(username=username).first()
            if user_data and bcrypt.checkpw(password, user_data.password):
                user = User(user_data.id)
                login_user(user)
                flash("You were successfully logged in")
                next = request.args.get("next")
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for("home"))
            else:
                error = "Login failed"
        return render_template("login.html", form=form, error=error)
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