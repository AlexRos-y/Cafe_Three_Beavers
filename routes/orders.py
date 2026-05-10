from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Order, OrderItem, CartItem
from datetime import datetime

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Ваша корзина пуста!', 'warning')
        return redirect(url_for('cart.cart'))

    total = sum(item.menu_item.price * item.quantity for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)

    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not delivery_address:
            flash('Укажите адрес доставки!', 'danger')
            return render_template('order.html', cart_items=cart_items, total=total, cart_count=cart_count)

        order = Order(
            user_id=current_user.id,
            total_price=total,
            delivery_address=delivery_address,
            latitude=latitude,
            longitude=longitude,
            status='new',
            created_at=datetime.utcnow()
        )
        db.session.add(order)
        db.session.flush()

        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=cart_item.menu_item_id,
                quantity=cart_item.quantity,
                price_per_unit=cart_item.menu_item.price
            )
            db.session.add(order_item)

        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash('Заказ успешно оформлен! Ожидайте доставку.', 'success')
        return redirect(url_for('orders.orders'))

    return render_template('order.html', cart_items=cart_items, total=total, cart_count=cart_count)


@orders_bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    cart_count = sum(item.quantity for item in current_user.cart_items)
    return render_template('orders.html', orders=user_orders, cart_count=cart_count)
