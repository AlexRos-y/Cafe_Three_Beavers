from flask import Blueprint, render_template, request
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
    return render_template('menu.html', items=items, categories=categories)