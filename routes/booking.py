from flask import Blueprint

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/booking')
def booking():
    return "Booking page - coming soon"