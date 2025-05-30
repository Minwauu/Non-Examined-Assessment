from extensions import db, bcrypt
from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Movie, Screening, SeatBooking, Showtime, SeatStatus
from functools import wraps
from seating import Seating

main_bp = Blueprint('main', __name__)

# function to ensure certain routes can only be accessed by staff/admin
def admin_required(view_function):
    @wraps(view_function)
    def wrapper():
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('This page is for staff only. Log in with your admin account.', 'danger')
            return redirect(url_for('main.login'))
        return view_function()
    return wrapper

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
            
            if user.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:    
            flash('Incorrect email or password', 'danger')
    
    return render_template('admin/login.html')
 
#dashboard page
@main_bp.route('/dashboard')
@login_required # need to be logged in to access dashboard

def dashboard():
    #display movies from db
    try:
        movies = Movie.query.all() 
        return render_template('admin/dashboard.html', username = current_user.username, movies = movies)
    except:
        flash('Error loading movies.', 'danger')
    return render_template('admin/dashboard.html', username=current_user.username, movies = [])
  

@main_bp.route('/logout')
@login_required # need to be logged in to log out

def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/add_movie', methods = ['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    #details
    if request.method =='POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        genre = request.form['genre']
        url = request.form['url']

        #make new movie using movie model
        new_movie = Movie(title=title, duration = duration, description = description, genre=genre, url=url)

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
@admin_required

def admin_dashboard():
    try:
        movies = Movie.query.all()
        screenings = Screening.query.all()
        #gets from db

        return render_template('admin/admindashboard.html', movies=movies, screenings=screenings, username = current_user.username)
    
    except Exception as e:
        flash('Error.', 'danger')
        return render_template('admin/admindashboard.html', movies=[], screenings=[])

@main_bp.route('/edit_movie', methods = ['POST', 'GET'])
@login_required
@admin_required

def edit_movie():
    if request.method == 'POST':
        try: 
            movie_id = request.form['movie_id']
            movie = Movie.query.get(movie_id)

            #details
            movie.title = request.form['title']
            movie.description = request.form['description']
            movie.duration = request.form['duration']
            movie.genre = request.form['genre']
        
            db.session.commit()
            flash('Movie edited successfully', 'success')
            return redirect(url_for('main.admin_dashboard'))
       
        except:
            db.session.rollback()
            flash('Error - try again.')
            return redirect(url_for('main.edit_movie', movie_id=movie_id))
       
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)
    return render_template('admin/editmovie.html', movie = movie)

@main_bp.route('/delete_movie', methods = ['GET', 'POST'])
@login_required
@admin_required

def delete_movie():
    if request.method == 'POST':
        try:
            movie_id = request.form['movie_id']
            movie = Movie.query.get(movie_id)

            if movie:
                db.session.delete(movie)
                db.session.commit()

                flash('Movie deleted successfully', 'success')
            else:
                flash('Movie not found - check spelling or try a different title', 'danger')   

        except:   
            db.session.rollback()
            flash('Error - try again.', 'danger')     

        return redirect(url_for('main.admin_dashboard'))
    
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)
    return render_template('admin/deletemovie.html', movie=movie)

@main_bp.route('/edit_screening', methods= ['GET', 'POST'])
@login_required
@admin_required

def edit_screening():
    
    screening_id = request.args.get('screening_id')
    screening= Screening.query.get(screening_id)
# if there isnt a screening go back to dashboard
    if not screening:
        flash("Screening was not found.", "danger")
        return redirect(url_for('main.admin_dashboard'))
    
    if request.method == "POST":
        try:
            screening_movie_id = request.form['movie_id']
            screening.screen_number= request.form['screen_number']

            db.session.commit()
            flash('Screening edited successfully.', 'success')
            return redirect(url_for('main.admin_dashboard'))
        except:
            db.session.rollback #if fails undo
            flash('Error - try again.', 'danger')
            return redirect(url_for('main.edit_screening', screening_id = screening.id))
        
    movies = Movie.query.all() # pick for screening
    return render_template('admin/editscreening.html', screening = screening, movies=movies)

@main_bp.route('/select_screening')
@login_required

def select_screening():
    movie_id = request.args.get('movie_id')

    if not movie_id:
        flash("Please pick a movie.", 'danger')
        return redirect(url_for('main.dashboard'))
    
    movie = Movie.query.get(movie_id)
    screenings = Screening.query.filter_by(movie_id = movie_id).all()
    return render_template('admin/selectscreening.html', movie=movie, screenings=screenings)

@main_bp.route('/select_seats')
@login_required

def select_seats():
    screening_id = request.args.get('screening_id')
    if not screening_id:
        flash("Please select a screening.", 'danger') # if no screening select
        return redirect(url_for('main.dashboard'))
    screening = Screening.query.get(screening_id)
    
    if not screening:
        flash('Unable to locate screening', 'danger')
        return redirect(url_for('main.dashboard'))
    
    booked_seats = SeatBooking.query.filter_by(screening_id=screening.id).with_entities(SeatBooking.seat_number).all()
    booked_seats = [seat[0] for seat in booked_seats]

    return render_template('admin/selectseats.html', screening = screening, booked_seats = booked_seats)

@main_bp.route('/book_seat', methods = ['POST', 'GET'])
@login_required

def book_seat():
    try:
        showtime_id = request.args.get('showtime_id')

        if not showtime_id:
            flash('No showtime given.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        showtime = Showtime.query.get(showtime_id)

        if not showtime:
            flash('Unable to locate showtime', 'danger')
            return redirect(url_for('main.dashboard'))
        
    
        screening = showtime.screening
        movie = screening.movie

        seating = Seating(showtime_id)
        all_seats = seating.seat_numbers() #gets all seats
        Booked_Seats = seating.booked_seats(db.session, SeatBooking) #gets booked seats
        Available_Seats = seating.available_seats(db.session, SeatBooking) #gets available seats
        Accessible_Seats = seating.accessibility_seats()

        needs_accessible = request.form.get('needs_accessible') if request.method == 'POST' else False

        
        if request.method =="POST":# if user selects seat
            selected_seats = request.form.getlist('seats')

            if selected_seats:
                unsuccessful_seats = []

                # checking if the seats the user picked are booked
                for seat in selected_seats:
                    if seat not in Booked_Seats:
                        booking = SeatBooking(showtime_id = showtime.id, seat_number =seat, user_id=current_user.id , screening_id = screening.id, availability=SeatStatus.AVAILABLE )
                        db.session.add(booking)
                    else:
                        unsuccessful_seats.append(seat) # seats that were unable to be booked
                    
                db.session.commit()
                if unsuccessful_seats:
                        
                    flash(f'Some seats were already taken: {", ".join(unsuccessful_seats)}.', 'warning')
                   
                else:
                    flash(f'Successfully booked {", ".join(selected_seats)}.', 'success')

                return redirect(url_for('main.dashboard'))

            else:
                flash('Please choose at least one seat.', 'danger')

        
        return render_template('admin/bookseat.html',screening = screening, movie= movie, showtime=showtime, all_seats = all_seats, Booked_Seats = Booked_Seats, Available_Seats = Available_Seats, Accessible_Seats = Accessible_Seats)
    
    except Exception as e:
        flash(f'Error: {str(e)} - try again.', 'danger')
        return redirect(url_for('main.dashboard'))
    

@main_bp.route('/my_bookings')
@login_required

def my_bookings():
    try: # get all bookings for user currently logged in
        bookings = SeatBooking.query.filter_by(user_id=current_user.id).all()

        #details of the movies
        bookings_details = []
        for booking in bookings:
            showtime = Showtime.query.get(booking.showtime_id)
            screening = showtime.screening
            movie = screening.movie
            bookings_details.append({'seat_number': booking.seat_number, 'movie_title': movie.title, 'screening_time': showtime.start_time, 'screen_number': screening.screen_number})
        return render_template('admin/mybookings.html', bookings = bookings_details)
    
    except Exception as e:
        #flash('Error showing bookings.', 'danger')
        flash(f'Error: {str(e)} - try again.', 'danger')
        return redirect(url_for('main.dashboard'))

    





