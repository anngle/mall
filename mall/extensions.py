# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_wechatpy import Wechat
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_restless import APIManager

from concurrent.futures import ThreadPoolExecutor

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
ckeditor = CKEditor()
wechat = Wechat()
mail = Mail()
executor = ThreadPoolExecutor()

api_manager = APIManager(flask_sqlalchemy_db=db)


login_manager.session_protection ='basic'
login_manager.login_view = 'auth.autologin'
login_manager.login_message = ""
login_manager.refresh_view = 'auth.autologin'
