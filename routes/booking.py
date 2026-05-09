from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Booking
from datetime import datetime, date, time

booking_bp = Blueprint('booking', __name__)

TABLES = {
    1: {'name': 'Столик 1', 'seats': 2, 'location': 'У окна', 'row': 0, 'col': 0},
    2: {'name': 'Столик 2', 'seats': 2, 'location': 'У окна', 'row': 0, 'col': 1},
    3: {'name': 'Столик 3', 'seats': 4, 'location': 'Центр', 'row': 0, 'col': 2},
    4: {'name': 'Столик 4', 'seats': 4, 'location': 'Центр', 'row': 0, 'col': 3},
    5: {'name': 'Столик 5', 'seats': 6, 'location': 'У камина', 'row': 1, 'col': 0},
    6: {'name': 'Столик 6', 'seats': 6, 'location': 'У камина', 'row': 2, 'col': 0},
    7: {'name': 'Столик 7', 'seats': 2, 'location': 'Бар', 'row': 1, 'col': 2},
    8: {'name': 'Столик 8', 'seats': 2, 'location': 'Бар', 'row': 1, 'col': 3},
    9: {'name': 'VIP-кабинка', 'seats': 8, 'location': 'VIP', 'row': 2, 'col': 2},
}


def get_ascii_map(booked_tables):
    grid = [
        ['[1]', '[2]', '[3]', '[4]'],
        ['[5]', '   ', '[7]', '[8]'],
        ['[6]', '   ', '[9]', '   '],
    ]
    
    result_grid = []
    for r in range(3):
        row = []
        for c in range(4):
            cell = grid[r][c]
            if cell.startswith('['):
                table_num = int(cell[1])
                if table_num in booked_tables:
                    cell = '[-]'  # Занят
                else:
                    cell = '[+]'  # Свободен
            row.append(cell)
        result_grid.append(row)
    
    ascii_map = f"""
┌─────────────────────────────────────────────────────────┐
│                      THREE BEAVERS CAFE                 │
│                                                         │
│   ОКНА          ОКНА         ОКНА        ОКНА           │
│ ┌─────────┐  ┌────────┐  ┌──────────┐ ┌──────────┐      │
│ │ Стол 1  │  │ Стол 2 │  │ Стол 3   │ │ Стол 4   │      │
│ │  2 мест │  │  2 мест│  │  4 места │ │  4 места │      │
│ │         |  |        |  |          | |          |      |
│ └─────────┘  └────────┘  └──────────┘ └──────────┘      │
│                                                         │
│ ┌─────────────────────┐              ┌─────────────────┐│
│ │     Стол 5          │              │    БАРНАЯ       ││
│ │     6 мест          │              │ ┌──────┐ ┌────┐ ││
│ │    (У КАМИНА)       │              │ │Стол 7│ │Ст 8│ ││
│ │                     |              | |      | |    | ||
│ └─────────────────────┘              │ └──────┘ └────┘ ││
│                                      └─────────────────┘│
│ ┌─────────────────────┐                                 │
│ │     Стол 6          │    ┌──────────────────┐         │
│ │     6 мест          │    │    VIP-КАБИНА    │         │
│ │    (У КАМИНА)       │    │    Стол 9        │         │
│ │                     │    │    8 мест        │         │
│ └─────────────────────┘    │                  │         │
│                            └──────────────────┘         │
└─────────────────────────────────────────────────────────┘
    """
    return ascii_map


@booking_bp.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        booking_date = request.form.get('date')
        time_from = request.form.get('time_from')
        time_to = request.form.get('time_to')
        table_number = request.form.get('table_number', type=int)
        phone = request.form.get('phone')
        special_requests = request.form.get('special_requests', '')
        errors = []
        
        if not booking_date:
            errors.append('Выберите дату')
        else:
            booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
        
        if not time_from or not time_to:
            errors.append('Выберите время')
        
        if not table_number or table_number not in TABLES:
            errors.append('Выберите столик')
        
        phone_clean = phone.replace(' ', '').replace('+', '').replace('(', '').replace(')', '').replace('-', '')
        if not phone or len(phone_clean) < 11:
            errors.append('Введите корректный номер телефона')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('booking.booking'))
        
        time_from_obj = datetime.strptime(time_from, '%H:%M').time()
        time_to_obj = datetime.strptime(time_to, '%H:%M').time()
        
        conflict = Booking.query.filter(
            Booking.date == booking_date_obj,
            Booking.table_number == table_number,
            Booking.status != 'cancelled',
            Booking.time_from < time_to_obj,
            Booking.time_to > time_from_obj
        ).first()
        
        if conflict:
            flash(f'Столик №{table_number} уже забронирован на это время!', 'danger')
            return redirect(url_for('booking.booking'))
        
        booking = Booking(
            user_id=current_user.id,
            date=booking_date_obj,
            time_from=time_from_obj,
            time_to=time_to_obj,
            table_number=table_number,
            phone=phone,
            special_requests=special_requests,
            status='pending',
            created_at=datetime.utcnow()
        )
        db.session.add(booking)
        db.session.commit()
        
        flash(f'Столик №{table_number} успешно забронирован на {booking_date} с {time_from} до {time_to}!', 'success')
        return redirect(url_for('booking.my_bookings'))
    
    today = date.today()
    bookings_today = Booking.query.filter(
        Booking.date == today,
        Booking.status != 'cancelled'
    ).all()
    
    now = datetime.utcnow().time()
    booked_tables = [b.table_number for b in bookings_today if b.time_from <= now <= b.time_to]
    
    ascii_map = get_ascii_map(booked_tables)
    
    return render_template('booking.html', 
                         tables=TABLES, 
                         booked_tables=booked_tables, 
                         today=today,
                         ascii_map=ascii_map)


@booking_bp.route('/my_bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date.desc(), Booking.time_from.desc()).all()
    now = datetime.utcnow()
    
    for b in bookings:
        booking_datetime = datetime.combine(b.date, b.time_to)
        if booking_datetime < now and b.status in ['pending', 'confirmed']:
            b.status = 'completed'
    
    db.session.commit()
    
    return render_template('my_bookings.html', bookings=bookings, tables=TABLES)


@booking_bp.route('/api/booked_tables')
def booked_tables_api():
    """API для проверки занятости столиков"""
    date_str = request.args.get('date')
    time_from = request.args.get('time_from')
    time_to = request.args.get('time_to')
    
    if not date_str or not time_from or not time_to:
        return jsonify({'error': 'Нужны date, time_from, time_to'}), 400
    
    booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    time_from_obj = datetime.strptime(time_from, '%H:%M').time()
    time_to_obj = datetime.strptime(time_to, '%H:%M').time()
    
    conflicts = Booking.query.filter(
        Booking.date == booking_date,
        Booking.status != 'cancelled',
        Booking.time_from < time_to_obj,
        Booking.time_to > time_from_obj
    ).all()
    
    booked = [b.table_number for b in conflicts]
    return jsonify({'booked_tables': booked})


@booking_bp.route('/api/ascii_map')
def ascii_map_api():
    """API для получения обновлённой ASCII-схемы"""
    date_str = request.args.get('date')
    time_from = request.args.get('time_from')
    time_to = request.args.get('time_to')
    
    if not date_str or not time_from or not time_to:
        return jsonify({'error': 'Нужны date, time_from, time_to'}), 400
    
    booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    time_from_obj = datetime.strptime(time_from, '%H:%M').time()
    time_to_obj = datetime.strptime(time_to, '%H:%M').time()
    
    conflicts = Booking.query.filter(
        Booking.date == booking_date,
        Booking.status != 'cancelled',
        Booking.time_from < time_to_obj,
        Booking.time_to > time_from_obj
    ).all()
    
    booked = [b.table_number for b in conflicts]
    ascii_map = get_ascii_map(booked)
    
    return jsonify({'ascii_map': ascii_map, 'booked_tables': booked})