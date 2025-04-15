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
    def booked_seats(self, db_session, SeatBookingModel):
        Booked_Seats = []
        booked = db_session.query(SeatBookingModel.seat_number).filter_by(showtime_id = self.showtime_id).all()
        for x in booked:
            Booked_Seats.append(x[0])
        return Booked_Seats
 #seats that are left   
    def available_seats(self, db_session, SeatBookingModel):
        available_seats = []
        all_seats = self.seat_numbers()
        Booked_Seats = self.booked_seats(db_session, SeatBookingModel)
        for y in all_seats:
            if y not in Booked_Seats:
                available_seats.append(y)
        return available_seats
# checks the availability of the seat    
    def check_if_booked(self, db_session, SeatBookingModel, seat_number):
        seat_booked = db_session.query(SeatBookingModel).filter_by(showtime_id= self.showtime_id, seat_number = seat_number).first()
        if seat_booked:
            return True
        else:
            return False
        


