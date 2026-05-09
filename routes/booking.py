from flask import Blueprint, render_template
from flask_login import login_required, current_user

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking')
@login_required
def booking():
    return render_template('booking.html')

@booking_bp.route('/my_bookings')
@login_required
def my_bookings():
    return render_template('my_bookings.html')