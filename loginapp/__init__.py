from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import configparser
import os

CONFIG_OPTIONS = {
    "DEBUG": False,
    "HOST": "127.0.0.1",
    "PORT": 5000,
    "SECRET_KEY": "update_me",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///users.db"
}

def parse_config():
    config = configparser.ConfigParser()

    conffile = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "../default.cfg")

    try:
        config.read(conffile)
    except:
        # need to setup logging
        print("Config file not found")

    for i in config["Default Configuration"]:
        CONFIG_OPTIONS[i.upper()] = config["Default Configuration"][i.upper()]

parse_config()

# flask app setup
app = Flask("loginapp")
app.secret_key = CONFIG_OPTIONS["SECRET_KEY"]
app.config["DEBUG"] = CONFIG_OPTIONS["DEBUG"]
app.config["HOST"] = CONFIG_OPTIONS["HOST"]
app.config["PORT"] = CONFIG_OPTIONS["PORT"]

# setup flask sqlalchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = CONFIG_OPTIONS["SQLALCHEMY_TRACK_MODIFICATIONS"]
app.config["SQLALCHEMY_DATABASE_URI"] = eval(CONFIG_OPTIONS["SQLALCHEMY_DATABASE_URI"])
db = SQLAlchemy(app)

# flask-login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

import loginapp.views