from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

#flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minwauu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema_booking_system.db'

# initialise and encrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

from admin import *

#runs
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)








    






