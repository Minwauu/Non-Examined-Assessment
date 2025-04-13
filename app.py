from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from extensions import db, bcrypt, login_manager
from flask_migrate import Migrate 


#flask setup
app = Flask(__name__, template_folder = 'templates')
app.config['SECRET_KEY'] = 'minwauu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema_booking_system.db'


db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app,db)

@login_manager.user_loader
def user_loader(user_id):
    from models import User
    return User.query.get(int(user_id))

from admin import main_bp
app.register_blueprint(main_bp)

from models import *

#runs
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

