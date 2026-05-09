from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, CartItem, MenuItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Считаем общую сумму
    total = sum(item.menu_item.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/cart/add/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    
    # Проверяем, есть ли уже такой товар в корзине
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        menu_item_id=item_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            menu_item_id=item_id,
            quantity=1
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{menu_item.name} добавлен в корзину!', 'success')
    return redirect(url_for('menu.menu'))

@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    cart_item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    # Возвращаем обновлённую сумму
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.menu_item.price * item.quantity for item in cart_items)
    
    return jsonify({'status': 'ok', 'total': total})

@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('Товар удалён из корзины', 'info')
    return redirect(url_for('cart.cart'))