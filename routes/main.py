from flask import Blueprint, render_template
from flask_login import current_user
from models import MenuItem

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    popular_items = MenuItem.query.filter_by(available=True).limit(4).all()
    return render_template('index.html', popular_items=popular_items)