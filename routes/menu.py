from flask import Blueprint, render_template, request
from flask_login import current_user
from models import MenuItem, Category

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/menu')
def menu():
    category_id = request.args.get('category', type=int)

    if category_id:
        items = MenuItem.query.filter_by(available=True, category_id=category_id).all()
    else:
        items = MenuItem.query.filter_by(available=True).all()

    categories = Category.query.all()
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = sum(item.quantity for item in current_user.cart_items)

    return render_template('menu.html', items=items, categories=categories, cart_count=cart_count)
