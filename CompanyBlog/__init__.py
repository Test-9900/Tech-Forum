#CompanyBlog / __init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

#############################################################
##################### DATABASE SETUP ########################
#############################################################


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)




#############################################################
##################### LOGIN CONFIGS #########################
#############################################################

loginManager = LoginManager()

loginManager.init_app(app)
loginManager.login_view = 'users.login'





from CompanyBlog.Core.views import core
from CompanyBlog.ErrorPages.handlers import errorPages
from CompanyBlog.Users.views import users
from CompanyBlog.BlogPosts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(errorPages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
