from flask import Blueprint

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews')
def reviews():
    return "Reviews page - coming soon"