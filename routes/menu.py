from flask import Blueprint

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def menu():
    return "Menu page - coming soon"