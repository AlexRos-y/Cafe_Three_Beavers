from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return "Login page - coming soon"

@auth_bp.route('/register')
def register():
    return "Register page - coming soon"

@auth_bp.route('/logout')
def logout():
    return "Logout - coming soon"