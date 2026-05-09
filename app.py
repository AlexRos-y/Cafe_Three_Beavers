from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from routes.auth import auth_bp
    from routes.menu import menu_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp
    from routes.booking import booking_bp
    from routes.reviews import reviews_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    @app.context_processor
    def inject_cart_count():
        from flask_login import current_user
        cart_count = 0
        if current_user.is_authenticated:
            cart_count = sum(item.quantity for item in current_user.cart_items)
        return {'cart_count': cart_count}
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)