from flask import Blueprint, render_template
from flask_login import login_required, current_user

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def cart():
    return render_template('cart.html')