from flask import Flask
from flask_login import LoginManager
import os
from .db import get_db 
from .models import User 

really_secret_key = os.urandom(32)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=really_secret_key, 
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # start database
    from . import db
    db.init_app(app)
    

    from . import auth
    app.register_blueprint(auth.bp)
    
    from .views import views 
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        user_row = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        if user_row:
            return User.from_db_row(user_row)  ##converts rows to a user object??
        return None

    return app
