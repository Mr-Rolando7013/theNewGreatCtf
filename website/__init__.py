from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/thegreatctf'
csrf = CSRFProtect(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

def create_app():

    db.init_app(app)
    #app.jinja_env.globals.update(delete_note)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()
    
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
