from flask import Blueprint, render_template
from flask_login import login_required, current_user

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/order')
@login_required
def order():
    return render_template('order.html')

@orders_bp.route('/orders')
@login_required
def orders():
    return render_template('orders.html')