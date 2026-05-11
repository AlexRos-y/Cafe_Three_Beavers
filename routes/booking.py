from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Booking
from forms import BookingForm
from datetime import datetime, date

booking_bp = Blueprint("booking", __name__)

TABLES = {
    1: {"name": "Столик 1", "seats": 2, "location": "У окна", "row": 0, "col": 0},
    2: {"name": "Столик 2", "seats": 2, "location": "У окна", "row": 0, "col": 1},
    3: {"name": "Столик 3", "seats": 4, "location": "Центр", "row": 0, "col": 2},
    4: {"name": "Столик 4", "seats": 4, "location": "Центр", "row": 0, "col": 3},
    5: {"name": "Столик 5", "seats": 6, "location": "У камина", "row": 1, "col": 0},
    6: {"name": "Столик 6", "seats": 6, "location": "У камина", "row": 2, "col": 0},
    7: {"name": "Столик 7", "seats": 2, "location": "Бар", "row": 1, "col": 2},
    8: {"name": "Столик 8", "seats": 2, "location": "Бар", "row": 1, "col": 3},
    9: {"name": "VIP-кабинка", "seats": 8, "location": "VIP", "row": 2, "col": 2},
}


def get_ascii_map(booked_tables):
    grid = [
        ["[1]", "[2]", "[3]", "[4]"],
        ["[5]", "   ", "[7]", "[8]"],
        ["[6]", "   ", "[9]", "   "],
    ]

    result_grid = []
    for r in range(3):
        row = []
        for c in range(4):
            cell = grid[r][c]
            if cell.startswith("["):
                table_num = int(cell[1])
                if table_num in booked_tables:
                    cell = "[-]"
                else:
                    cell = "[+]"
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


def get_booked_tables(booking_date, time_from, time_to):
    conflicts = Booking.query.filter(
        Booking.date == booking_date,
        Booking.status != "cancelled",
        Booking.time_from < time_to,
        Booking.time_to > time_from
    ).all()
    return [b.table_number for b in conflicts]


@booking_bp.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    form = BookingForm()

    check_date_str = request.args.get("check_date", date.today().strftime("%Y-%m-%d"))
    check_time_from = request.args.get("check_time_from", "10:00")
    check_time_to = request.args.get("check_time_to", "12:00")

    try:
        check_date = datetime.strptime(check_date_str, "%Y-%m-%d").date()
        check_time_from_obj = datetime.strptime(check_time_from, "%H:%M").time()
        check_time_to_obj = datetime.strptime(check_time_to, "%H:%M").time()
        booked_tables = get_booked_tables(check_date, check_time_from_obj, check_time_to_obj)
    except:
        booked_tables = []

    if form.validate_on_submit():
        booking_date_obj = form.date.data
        time_from_obj = datetime.strptime(form.time_from.data, "%H:%M").time()
        time_to_obj = datetime.strptime(form.time_to.data, "%H:%M").time()
        table_number = int(form.table_number.data)

        # Check for conflicts
        conflict = Booking.query.filter(
            Booking.date == booking_date_obj,
            Booking.table_number == table_number,
            Booking.status != "cancelled",
            Booking.time_from < time_to_obj,
            Booking.time_to > time_from_obj
        ).first()

        if conflict:
            flash(f"Столик №{table_number} уже забронирован на это время!", "danger")
            return redirect(url_for("booking.booking"))

        booking = Booking(
            user_id=current_user.id,
            date=booking_date_obj,
            time_from=time_from_obj,
            time_to=time_to_obj,
            table_number=table_number,
            phone=form.phone.data,
            special_requests=form.special_requests.data,
            status="pending",
            created_at=datetime.utcnow()
        )
        db.session.add(booking)
        db.session.commit()

        flash(f"Столик №{table_number} успешно забронирован!", "success")
        return redirect(url_for("booking.my_bookings"))

    today = date.today()
    ascii_map = get_ascii_map(booked_tables)

    return render_template("booking.html",
                           form=form,
                           tables=TABLES,
                           booked_tables=booked_tables,
                           today=today,
                           ascii_map=ascii_map,
                           check_date=check_date_str,
                           check_time_from=check_time_from,
                           check_time_to=check_time_to)


@booking_bp.route("/my_bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(
        Booking.date.desc(), Booking.time_from.desc()
    ).all()

    now = datetime.utcnow()
    for b in bookings:
        booking_datetime = datetime.combine(b.date, b.time_to)
        if booking_datetime < now and b.status in ["pending", "confirmed"]:
            b.status = "completed"
    db.session.commit()

    return render_template("my_bookings.html", bookings=bookings, tables=TABLES)
