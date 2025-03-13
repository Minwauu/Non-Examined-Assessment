from app import app, db, bcrypt
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from model import User

# registration page
@app.route('/registering', methods = ['GET', 'POST'])
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
            return redirect(url_for('registering'))
        #checks email
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('registering'))
        
        #adds new user to database
        new_user = User(username=username, email = email, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registeration complete - log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registering.html')

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password): #checks if email and password is correct
            flash('Login complete!', 'success')
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password', 'danger')
    
    return render_template('login.html')

#dashboard page
@app.route('/dashboard')
@login_required # need to be logged in to access dashboard

def dashboard():
    return render_template('dashboard.html', username=current_user.username)
  

@app.route('/logout')
@login_required # need to be logged in to log out

def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))
