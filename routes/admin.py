from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Order, OrderItem, Booking, MenuItem, Category, Review
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os
import uuid

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Доступ запрещён! Только для администраторов.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    today = date.today()
    
    stats = {
        'new_orders': Order.query.filter_by(status='new').count(),
        'active_orders': Order.query.filter(Order.status.in_(['new', 'preparing', 'ready'])).count(),
        'today_bookings': Booking.query.filter_by(date=today).count(),
        'pending_bookings': Booking.query.filter_by(status='pending').count(),
        'total_users': User.query.count(),
        'total_menu': MenuItem.query.count(),
    }
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    today_bookings = Booking.query.filter_by(date=today).order_by(Booking.time_from).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_orders=recent_orders,
                         today_bookings=today_bookings,
                         today=today)


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    status_filter = request.args.get('status', 'all')
    
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    all_orders = query.all()
    statuses = ['new', 'preparing', 'ready', 'delivered', 'cancelled']
    
    return render_template('admin/orders.html', 
                         orders=all_orders, 
                         current_filter=status_filter,
                         statuses=statuses)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['new', 'preparing', 'ready', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Статус заказа #{order.id} изменён на «{new_status}»', 'success')
    
    return redirect(url_for('admin.orders'))


@admin_bp.route('/bookings')
@login_required
@admin_required
def bookings():
    date_filter = request.args.get('date', '')
    status_filter = request.args.get('status', 'all')
    
    query = Booking.query.order_by(Booking.date, Booking.time_from)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if date_filter:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        query = query.filter_by(date=filter_date)
    else:
        query = query.filter(Booking.date >= date.today())
    
    all_bookings = query.all()
    
    return render_template('admin/bookings.html', 
                         bookings=all_bookings,
                         current_date=date_filter,
                         current_status=status_filter,
                         today=date.today())


@admin_bp.route('/bookings/<int:booking_id>/status', methods=['POST'])
@login_required
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        booking.status = new_status
        db.session.commit()
        flash(f'Статус брони #{booking.id} изменён на «{new_status}»', 'success')
    
    return redirect(url_for('admin.bookings'))



@admin_bp.route('/menu')
@login_required
@admin_required
def menu():
    items = MenuItem.query.order_by(MenuItem.category_id, MenuItem.name).all()
    categories = Category.query.all()
    return render_template('admin/menu.html', items=items, categories=categories)


@admin_bp.route('/menu/add', methods=['POST'])
@login_required
@admin_required
def add_menu_item():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    price = request.form.get('price', type=float)
    category_id = request.form.get('category_id', type=int)
    
    if not name or not price or not category_id:
        flash('Заполните все обязательные поля!', 'danger')
        return redirect(url_for('admin.menu'))
    image_url = 'default-food.jpg'
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                upload_folder = os.path.join(current_app.static_folder, 'images', 'menu')
                filepath = os.path.join(upload_folder, unique_name)
                file.save(filepath)
                image_url = unique_name
    
    item = MenuItem(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        image_url=image_url,
        available=True
    )
    db.session.add(item)
    db.session.commit()
    
    flash(f'Блюдо «{name}» добавлено в меню!', 'success')
    return redirect(url_for('admin.menu'))


@admin_bp.route('/menu/<int:item_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    
    item.name = request.form.get('name', '').strip()
    item.description = request.form.get('description', '').strip()
    item.price = request.form.get('price', type=float)
    item.category_id = request.form.get('category_id', type=int)
    item.available = request.form.get('available') == 'on'

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                upload_folder = os.path.join(current_app.static_folder, 'images', 'menu')
                filepath = os.path.join(upload_folder, unique_name)
                file.save(filepath)
                if item.image_url and item.image_url != 'default-food.jpg':
                    old_path = os.path.join(upload_folder, item.image_url)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                item.image_url = unique_name
    
    db.session.commit()
    flash(f'Блюдо «{item.name}» обновлено!', 'success')
    return redirect(url_for('admin.menu'))


@admin_bp.route('/menu/<int:item_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(f'Блюдо «{name}» удалено из меню!', 'info')
    return redirect(url_for('admin.menu'))


@admin_bp.route('/menu/toggle/<int:item_id>', methods=['POST'])
@login_required
@admin_required
def toggle_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.available = not item.available
    db.session.commit()
    status = 'доступно' if item.available else 'скрыто'
    flash(f'Блюдо «{item.name}» теперь {status}', 'info')
    return redirect(url_for('admin.menu'))

@admin_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    OrderItem.query.filter_by(order_id=order.id).delete()
    db.session.delete(order)
    db.session.commit()
    flash(f'Заказ #{order_id} удалён!', 'info')
    return redirect(url_for('admin.orders'))


@admin_bp.route('/bookings/<int:booking_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash(f'Бронь #{booking_id} удалена!', 'info')
    return redirect(url_for('admin.bookings'))