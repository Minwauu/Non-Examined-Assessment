rows = ['A', 'B', 'C', 'D', 'E']
seats_per_row = 10


class Seating:
    # initialisation
    def __init__(self, showtime_id):
        self.showtime_id = showtime_id
        self.rows = rows
        self.seats_per_row = seats_per_row
# generate seat string
    def seat_numbers(self):
        seats = []
        for row in self.rows:
            for i in range(1, (self.seats_per_row+1)):
                seat_number = str(row) + str(i)
                seats.append(seat_number)
        return seats
 # list of taken seats (double book prevention)   
    def booked_seats(self, db_session, SeatBooking):
        Booked_Seats = []
        booked = db_session.query(SeatBooking.seat_number).filter_by(showtime_id = self.showtime_id).all()
        for x in booked:
            Booked_Seats.append(x[0])
        return Booked_Seats
 #seats that are left   
    def available_seats(self, db_session, SeatBooking):
        Available_Seats = []
        all_seats = self.seat_numbers()
        Booked_Seats = self.booked_seats(db_session, SeatBooking)
        for y in all_seats:
            if y not in Booked_Seats:
                Available_Seats.append(y)
        return Available_Seats
# checks the availability of the seat    
    def check_if_booked(self, db_session, SeatBooking, seat_number):
        seat_booked = db_session.query(SeatBooking).filter_by(showtime_id= self.showtime_id, seat_number = seat_number).first()
        if seat_booked:
            return True
        else:
            return False
        
    def accessibility_seats(self):
        return ['A1', 'A2', 'A9', 'A10']
        


