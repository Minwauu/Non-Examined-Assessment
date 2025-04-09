from extensions import db, bcrypt
from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Movie, Screening

main_bp = Blueprint('main', __name__)

# registration page
@main_bp.route('/registering', methods = ['GET', 'POST'])
def registering():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = User.query.filter_by(email=email).first()
        
        #checks username
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken.', 'danger')
            return redirect(url_for('main.registering'))
        #checks email
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('main.registering'))
        
        #adds new user to database
        new_user = User(username=username, email = email, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration complete - log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('admin/registering.html')

#login page
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password): #checks if email and password is correct
            flash('Login complete!', 'success')
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Incorrect email or password', 'danger')
    
    return render_template('admin/login.html')

#dashboard page
@main_bp.route('/dashboard')
@login_required # need to be logged in to access dashboard

def dashboard():
    return render_template('admin/dashboard.html', username=current_user.username)
  

@main_bp.route('/logout')
@login_required # need to be logged in to log out

def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/add_movie', methods = ['GET', 'POST'])
def add_movie():
    #details
    if request.method =='POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        genre = request.form['genre']

        #make new movie using movie model
        new_movie = Movie(title=title, duration = duration, description = description, genre=genre)

        try:
            # add movie to db
            db.session.add(new_movie)
            db.session.commit()
            flash('Success - Movie added.')
        except:
            #catching error
            db.session.rollback()
            flash('Error - Try again.')
        
        return redirect(url_for('main.add_movie'))
    
    return render_template('admin/addmovie.html') #defaults to form page

@main_bp.route('/admin_dashboard')
@login_required

def admin_dashboard():
    try:
        movies = Movie.query.all()
        screenings = Screening.query.all()
        #gets from db

        return render_template('admin/admindashboard.html', movies=movies, screenings=screenings)
    
    except:
        flash('Error.', 'danger')
        return render_template('admin/admindashboard.html', movies=[], screenings=[])



