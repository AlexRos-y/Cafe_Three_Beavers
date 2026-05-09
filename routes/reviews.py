from flask import Blueprint, render_template
from models import Review

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/reviews')
def reviews():
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', reviews=all_reviews)