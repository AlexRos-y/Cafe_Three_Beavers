from flask import Blueprint

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/order')
def order():
    return "Order page - coming soon"